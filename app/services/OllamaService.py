from app.models.model import ModelRequest
import subprocess
import ollama
import psutil
import time
from fastapi import HTTPException

class OllamaService:
    def __init__(self):
        self.start_ollama_server()
        self.installed_models = list(map(lambda model: model.model, ollama.list().models))

    def is_ollama_running(self) -> bool:
        """Check if the Ollama server is running."""
        for proc in psutil.process_iter(['cmdline']):
            if proc.info['cmdline'] and 'ollama' in proc.info['cmdline'] and 'serve' in proc.info['cmdline']:
                return True
        return False

    def start_ollama_server(self):
        """Start the Ollama server and wait until it's ready."""
        try:
            process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for _ in range(30):  # Retry up to 30 times (30 seconds)
                if self.is_ollama_running():
                    return  # Server is ready
                time.sleep(1)
            process.terminate()
            raise HTTPException(status_code=500, detail="Ollama server did not start within the expected time.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start Ollama server: {str(e)}")

    def install_model(self, model_name: str):
        """Install the specified model if not already installed."""
        if model_name not in self.installed_models:
            try:
                process = subprocess.Popen(
                    ["ollama", "pull", model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate(timeout=300)  # Wait up to 5 minutes
                if process.returncode != 0:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to install model: {model_name}. Error: {stderr.decode().strip()}"
                    )
                self.installed_models = ollama.list()
                if model_name not in self.installed_models:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Model {model_name} installation verification failed."
                    )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                raise HTTPException(
                    status_code=500,
                    detail=f"Model installation timed out: {model_name}. Error: {stderr.decode().strip()}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred during model installation: {str(e)}"
                )

    def is_model_installed(self, model_name: str) -> bool:
        """Check if the model name is a substring of any installed model names."""
        return any(model_name in installed_model for installed_model in self.installed_models)

    def query_model(self, model_name: str, prompt: str):
        """Query the specified model with the given prompt."""
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying model: {str(e)}")