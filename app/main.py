from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import subprocess
from app.models.model import ModelRequest
from app.services.OllamaService import OllamaService

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/install_and_query_model/")
async def install_and_query_model(request: ModelRequest):
    try:
        ollama_service = OllamaService()
        if not ollama_service.is_model_installed(request.modelName):
            ollama_service.install_model(request.modelName)
        response = ollama_service.query_model(request.modelName, request.prompt)
        async def event_stream():
            for part in response:
                yield f"data: {part['message']['content']}\n\n"
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Model installation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))