from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(title='ModelGate')

MODELS = [
    {"name": "Claude", "version": "latest"},
    {"name": "GPT-4", "version": "latest"},
    {"name": "LLaMA", "version": "latest"},
    {"name": "Mistral", "version": "latest"},
    {"name": "Falcon", "version": "latest"}
]

class ChatRequest(BaseModel):
    model: str
    prompt: str

@app.get("/")
def get():
    return {"message": "Hello, World!"}

@app.get('/healthz')
def health():
    return {"status": "healthy"}

@app.get('/v1/models')
def get_models():
    return {'models': MODELS}

@app.post('/v1/chat')
def chat(request: ChatRequest):
    model_name = request.model
    prompt = request.prompt

    # Checking if the requested model is available
    if model_name not in [model['name'] for model in MODELS]:
        raise HTTPException(status_code=404, detail=f"Model {model_name} doesn't exist")

    return {
        'model': model_name,
        'prompt': prompt,
        'response': f"Response from {model_name} for prompt: {prompt}"
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
    )