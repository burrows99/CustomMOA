from pydantic import BaseModel

class ModelRequest(BaseModel):
    modelName: str
    prompt: str