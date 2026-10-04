from app.providers.mock import MockProvider
from app.providers.registry import ProviderRegistry
from app.schemas import ChatRequest
from fastapi import FastAPI, HTTPException
import uvicorn
import os

app = FastAPI(title='ModelGate')
provider = ProviderRegistry()
provider.register("mock", MockProvider())

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
    try:
        response = provider.generate_response(request.model, request.prompt)
        return {
            "model": request.model,
            "prompt": request.prompt,
            "response": response
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
    )