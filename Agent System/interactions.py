# Functions for interacting with agents asynchronously.

import asyncio
import logging
from .sessions import runner
from google.genai import types

async def call_agent_async(query: str, runner):
    logging.info(f"call_agent_async called with query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."
    async for event in runner.run_async(user_id="user", session_id="session", new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
    return final_response_text

async def run_conversation():
    logging.info("run_conversation started")
    loop = asyncio.get_event_loop()
    while True:
        query = await loop.run_in_executor(None, input, "User(or 'exit' to quit): ")
        if query.lower() == 'exit':
            # Trigger goodbye response from agent
            response = await call_agent_async('goodbye', runner=runner)
            print(f"Agent: {response}")
            break
        response = await call_agent_async(query, runner=runner)
        print(f"Agent: {response}")

