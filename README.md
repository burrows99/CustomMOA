# Ollama Docker Setup

Run large language models locally using Docker and Ollama.

## Prerequisites
- Docker Engine 20.10+
- 4GB+ RAM (8GB recommended)
- Mac/Linux/Windows (WSL2)

## Quick Start

1. **Start the service**:
```bash
docker compose up -d
```

2. **Install a model** (TinyLlama example):
```bash
# Using Docker CLI
docker exec ollama ollama pull tinyllama

# Or using API
curl http://localhost:11434/api/pull -d '{
  "name": "tinyllama"
}'
```

3. **Use the API** (equivalent to Docker CLI commands):
```bash
# API request (same as 'docker exec ollama ollama run...')
curl http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

## API vs Docker CLI Equivalents

| Operation          | Docker CLI                          | API Endpoint       |
|--------------------|-------------------------------------|--------------------|
| Pull model         | `docker exec ollama ollama pull`    | `POST /api/pull`   |
| List models        | `docker exec ollama ollama list`    | `GET /api/tags`    |
| Remove model       | `docker exec ollama ollama rm`      | `DELETE /api/delete` |
| Run model          | `docker exec ollama ollama run`     | `POST /api/generate` or `/api/chat` |
| Model info         | `docker exec ollama ollama show`    | `POST /api/show`   |

All operations available through Docker CLI can be performed directly via API calls to `http://localhost:11434`.

## Ollama API Documentation

Base URL: `http://localhost:11434`

Full API documentation available at:  
[Ollama REST API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Managing Models (API Examples)

**List installed models**:
```bash
curl http://localhost:11434/api/tags
```

**Remove a model**:
```bash
curl -X DELETE http://localhost:11434/api/delete -d '{
  "name": "tinyllama"
}'
```

## Frontend Interface

A React-based UI for interacting with Ollama models through the containerized API.

![Interface Preview](./frontend/public/screenshot.png) <!-- Add screenshot later -->

### Features
- Chat interface for LLM conversations
- Model selection dropdown
- Response streaming support
- Conversation history

### Running the Full Stack

1. Start both containers:
```bash
docker compose up -d --build
```

2. Access the interfaces:
- **Frontend UI**: `http://localhost:3000`
- **Ollama API**: `http://localhost:11434`

### Development
```bash
# Frontend-specific commands
cd frontend
npm install
npm start
```

The frontend container automatically connects to the Ollama API container through Docker's internal network. No API key required for local development.

## Troubleshooting

- **Model not found**: Pull the model first `docker exec ollama ollama pull <name>`
- **Port conflict**: Change `11434` in `docker-compose.yml`
- **Low memory**: Use smaller models like `tinyllama` or `phi3` 