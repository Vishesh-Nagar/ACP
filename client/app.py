import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    translation = ""
    if request.method == "POST":
        phrase = request.form.get("phrase", "").strip()
        if phrase:
            # Prepare ACP-formatted payload
            payload = {
                "agent_name": "translator_agent",
                "input": [
                    {
                        "role": "user",
                        "parts": [
                            {"content": phrase, "content_type": "text/plain"}
                        ]
                    }
                ]
            }
            try:
                # Call the server's /runs endpoint (ACP-style)
                server_url = os.environ.get("SERVER_URL", "http://localhost:8000")
                resp = requests.post(
                    server_url + "/runs",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=15.0
                )
                resp.raise_for_status()
                data = resp.json()
                # Extract translation text from response
                output_parts = data.get("output", [])[0].get("parts", [])
                if output_parts:
                    translation = output_parts[0].get("content", "")
            except Exception as e:
                translation = f"Error: {e}"

    return render_template("index.html", translation=translation)

if __name__ == "__main__":
    app.run(port=5000)
