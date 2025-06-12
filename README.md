# ChatGPT-Unraid Assistant

A self-hosted assistant for your Unraid server powered by OpenAI GPT-4o.  
Ask questions about your system, get insights from logs, upload screenshots, and interact via a mobile-friendly web UI.

![screenshot](https://raw.githubusercontent.com/Gayb0iiiii/ChatGPT-Unraid/main/screenshot.png)

---

## 🚀 Features

- ✅ GPT-4o support using OpenAI's latest API
- 🔍 Analyzes:
  - System metrics (`uptime`, `df -h`, `free -m`)
  - Docker container status & logs
  - `/var/log/syslog` (or alternative)
- 🖼 Image upload support (e.g. system screenshots)
- 📱 Mobile-first responsive web UI
- 🧠 Configurable backend instructions via env var
- 🔐 API key input via container settings

---

## 🛠 Installation via Unraid CA

Use the [CA template](ChatGPT-Unraid-Final_CA_template.xml) and set:

| Variable            | Description                                 |
|---------------------|---------------------------------------------|
| `OPENAI_API_KEY`    | Your OpenAI API key (required)              |
| `INSTRUCTIONS`      | (Optional) System behavior prompt override  |

The assistant runs on port `5000`. Ensure it's mapped and accessible in Unraid.

---

## 🧪 Docker Build

```bash
docker build -t sweatyboi/unraidgpt-assistant .
docker run -d -p 5000:5000 \
  -e OPENAI_API_KEY=your_key \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /var/log:/var/log:ro \
  sweatyboi/unraidgpt-assistant
```

---

## 📁 File Structure

```
/backend
  app.py              # Flask backend + OpenAI logic
  requirements.txt    # Python dependencies
/templates
  index.html          # Frontend with image upload + chat UI
Dockerfile            # Container build script
ChatGPT-Unraid-Final_CA_template.xml  # CA-compatible installer
```

---

## 🧠 Behavior Customization

You can set a custom instruction string like:
```
-e INSTRUCTIONS="Respond with command-line solutions only."
```

If omitted, it defaults to:
> You are an expert Unraid assistant. Always respond helpfully and clearly. Summarize important findings. Use bullet points for clarity...

---

## 📷 Screenshots

See [`/screenshot.png`](https://github.com/Gayb0iiiii/ChatGPT-Unraid/blob/main/screenshot.png) for UI preview.

---

## 🤝 Support & Contributions

- GitHub: [ChatGPT-Unraid](https://github.com/Gayb0iiiii/ChatGPT-Unraid)
- Issues: [GitHub Issues](https://github.com/Gayb0iiiii/ChatGPT-Unraid/issues)

MIT License
