import subprocess
import ollama
import psutil
import time
from fastapi import HTTPException

class OllamaService:
    def __init__(self):
        self.start_ollama_server()
        self.installedModelNames = []
        self.update_installed_model_names_list()

    def update_installed_model_names_list(self):
        self.installedModelNames = list(map(lambda model: model.model, ollama.list().models))
        return self.installedModelNames

    def is_model_installed(self, modelName: str) -> bool:
        return modelName in self.installedModelNames


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
            for _ in range(30):
                if self.is_ollama_running():
                    return
                time.sleep(1)
            process.terminate()
            raise HTTPException(status_code=500, detail="Ollama server did not start within the expected time.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start Ollama server: {str(e)}")

    def install_model(self, modelName: str):
        """Install the specified model if not already installed."""
        if not self.is_model_installed(modelName):
            try:
                process = subprocess.Popen(
                    ["ollama", "pull", modelName],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate(timeout=300)
                if process.returncode != 0:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to install model: {modelName}. Error: {stderr.decode().strip()}"
                    )
                self.update_installed_model_names_list()
                if not self.is_model_installed(modelName):
                    raise HTTPException(
                        status_code=500,
                        detail=f"Model {modelName} installation verification failed."
                    )
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                raise HTTPException(
                    status_code=500,
                    detail=f"Model installation timed out: {modelName}. Error: {stderr.decode().strip()}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred during model installation: {str(e)}"
                )

    def is_model_installed(self, modelName: str) -> bool:
        """Check if the model name is a substring of any installed model names."""
        return any(modelName in installedModel for installedModel in self.installedModelNames)

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