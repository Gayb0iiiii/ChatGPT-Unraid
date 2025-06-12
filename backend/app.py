import os
import subprocess
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)


def run_cmd(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, check=True).stdout.decode()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {e.stderr.decode()}"


def get_system_context():
    return {
        "cpu": run_cmd("uptime") or "[Not available]",
        "disk": run_cmd("df -h") or "[Not available]",
        "mem": run_cmd("free -m") or "[Not available]",
        "syslog": run_cmd("tail -n 200 /var/log/syslog") or "[Not available]",
        "docker": run_cmd("docker ps --format '{{.Names}}'") or "[Docker not running]"
    }


def build_prompt(user_input, context):
    instructions = os.getenv("INSTRUCTIONS", "").strip() or (
        "You are an expert Unraid assistant. Always respond helpfully and clearly. "
        "Summarize important findings. Use bullet points for clarity. "
        "Refer to logs and system metrics accurately."
    )
    return (
        f"{instructions}\n\n"
        f"User question: '{user_input}'\n\n"
        f"== CPU ==\n{context['cpu']}\n"
        f"== DISK ==\n{context['disk']}\n"
        f"== MEMORY ==\n{context['mem']}\n"
        f"== DOCKER ==\n{context['docker']}\n"
        f"== SYSLOG ==\n{context['syslog']}"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/ask/image", methods=["POST"])
def ask_with_image():
    question = request.form.get("question", "")
    image = request.files.get("image")
    image_data = None

    if image:
        try:
            img = Image.open(image.stream)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            image_data = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_base64}"
                }
            }
        except Exception as e:
            return jsonify({"error": f"Image processing failed: {str(e)}"}), 400

    context = get_system_context()
    prompt = build_prompt(question, context)

    try:
        messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        if image_data:
            messages[0]["content"].append(image_data)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.5
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
