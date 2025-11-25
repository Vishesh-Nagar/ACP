import os
import uuid
import asyncio
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

app = Flask(__name__)

translator_agent = LlmAgent(
    name="translator_agent",
    model="gemini-2.5-flash",
    description="Translates English phrases to Spanish.",
    instruction="Translate the following English phrase to Spanish."
)

session_service = InMemorySessionService()
runner = Runner(
    agent=translator_agent,
    app_name="translator_app",
    session_service=session_service
)

@app.route("/agents", methods=["GET"])
def get_agents():
    return jsonify({
        "agents": [{
            "name": translator_agent.name,
            "description": translator_agent.description,
            "metadata": {}
        }]
    })

@app.route("/runs", methods=["POST"])
def run_agent():
    data = request.get_json()
    input_list = data.get("input", [])
    if not input_list:
        return jsonify({"error": "Missing 'input'"}), 400

    parts = input_list[0].get("parts", [])
    text = "".join(p.get("content", "") for p in parts)

    session_id = str(uuid.uuid4())
    # Await session creation
    asyncio.run(
        session_service.create_session(
            app_name="translator_app",
            user_id="user",
            session_id=session_id
        )
    )

    content = types.Content(
        role="user",
        parts=[ types.Part(text=text) ]
    )

    translation = ""
    for event in runner.run(
        user_id="user",
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            translation = event.content.parts[0].text
            break

    response = {
        "run_id": str(uuid.uuid4()),
        "agent_name": translator_agent.name,
        "session_id": session_id,
        "status": "completed",
        "output": [{
            "role": f"agent/{translator_agent.name}",
            "parts": [{
                "content": translation,
                "content_type": "text/plain"
            }]
        }],
        "error": None
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=8000)
