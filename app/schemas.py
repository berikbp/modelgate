# what requests/reponses data looks like
from pydantic import BaseModel


class ChatRequest(BaseModel):
    model: str
    prompt: str