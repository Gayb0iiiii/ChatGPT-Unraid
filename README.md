# Unraid ChatGPT Assistant

Talk to your Unraid system via ChatGPT. This container gathers system data (logs, Docker, disk/mem info) and provides intelligent responses.

## 🔧 Docker Run

```bash
docker run -d \
  -p 5000:5000 \
  -v /var/log:/var/log:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e OPENAI_API_KEY=sk-xxx \
  your_dockerhub_username/unraidgpt-assistant:latest
```

## 📡 Endpoints

- `POST /ask` with `{ "question": "..." }`
- `GET /ask/stream?question=...` for live stream
