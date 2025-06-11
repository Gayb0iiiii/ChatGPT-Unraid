backend/app.py
import os
import openai
import subprocess
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def run_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, check=True).stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"Error running '{cmd}': {e.stderr.decode()}"

def get_system_context():
    return {
        "cpu": run_cmd("uptime"),
        "disk": run_cmd("df -h"),
        "mem": run_cmd("free -m"),
        "syslog": run_cmd("tail -n 200 /var/log/syslog"),
        "docker": get_all_docker_logs()
    }

def get_all_docker_logs():
    logs = ""
    containers = run_cmd("docker ps --format '{{.Names}}'").splitlines()
    for name in containers:
        log = run_cmd(f"docker logs --tail 100 {name}")
        logs += f"Logs for {name}:\n{log}\n"
    return logs

def build_prompt(user_input, context):
    return f"""User question: "{user_input}"

System state summary:
- CPU load: {context['cpu']}
- Disk usage: {context['disk']}
- Memory: {context['mem']}
- Docker container logs: {context['docker']}
- System logs (last 200 lines): {context['syslog']}

Respond like a system assistant for Unraid with insight from the above logs.
"""


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    context = get_system_context()
    prompt = build_prompt(question, context)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask/stream", methods=["GET"])
def stream():
    question = request.args.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' query param"}), 400

    context = get_system_context()
    prompt = build_prompt(question, context)

    def generate():
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                stream=True
            )
            for chunk in response:
                delta = chunk['choices'][0]['delta']
                if "content" in delta:
                    yield f"data: {delta['content']}\n\n"

"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}

"

    return Response(generate(), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
