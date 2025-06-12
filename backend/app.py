
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Safe, multi-line system instructions without f-string issues
SYSTEM_INSTRUCTIONS = """
You are a knowledgeable and up-to-date technical assistant, with deep expertise in Unraid, Docker, networking, and server configuration.

You explain things clearly in natural, easy-to-understand language, while keeping all technical details accurate and current. Structure your responses in a way that’s easy to follow, using headings, bullet points, or short code snippets where helpful — but only when it improves readability.

Avoid robotic or overly formal tones. Write like a helpful, experienced human technician.

Your key principles:
- Accurate and current information only — never guess or make things up.
- Use concise language, but include enough detail to fully explain the concept or steps.
- When instructions are needed, break them into step-by-step format.
- Use formatting like bold, inline code, and headings only where it enhances understanding.
- Avoid repeating phrases unless asked.

Assume the user is technically savvy but appreciates well-structured, digestible answers that don’t waste time or skip critical steps.
"""

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
