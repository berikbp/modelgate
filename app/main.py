from app.providers.mock import MockProvider
from app.schemas import ChatRequest
from fastapi import FastAPI, HTTPException
import uvicorn
import os

app = FastAPI(title='ModelGate')
provider = MockProvider()

@app.get("/")
def get():
    return {"message": "Hello, World!"}

@app.get('/healthz')
def health():
    return {"status": "healthy"}

@app.get('/v1/models')
def get_models():
    return {'models': provider.list_models()}

@app.post('/v1/chat')
def chat(request: ChatRequest):
    model_name = request.model
    prompt = request.prompt

    # Checking if the requested model is available
    if model_name not in [model['name'] for model in provider.list_models()]:
        raise HTTPException(status_code=404, detail=f"Model {model_name} doesn't exist")

    response = provider.generate_response(model_name, prompt)
    return {
        'model': model_name,
        'prompt': prompt,
        'response': response
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
    )