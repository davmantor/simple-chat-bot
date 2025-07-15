from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
from typing import List

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL")
MODEL_NAME = os.getenv("ANTHROPIC_MODEL")

print(f"Loaded env variables:")
print(f"  API_KEY: {'set' if API_KEY else 'MISSING'}")
print(f"  BASE_URL: {BASE_URL}")
print(f"  MODEL_NAME: {MODEL_NAME}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    history: List[ChatMessage]

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    print("-"*100)
    print("Received chat request:")
    for msg in payload.history:
        print(f"  {msg.role}: {msg.content}")

    # specific to anthropic
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }

    payload_data = {
        "model": MODEL_NAME,
        "max_tokens": 300,
        "messages": [m.dict() for m in payload.history]
    }

    print("Sending payload to LLM:")
    print(payload_data)

    async with httpx.AsyncClient() as client:
        res = await client.post(BASE_URL, headers=headers, json=payload_data)

    print("Received response:")
    print(res.status_code)
    print(res.text)

    try:
        data = res.json()
        reply = data["content"][0]["text"]
        print("Parsed reply:", reply)
        return ChatResponse(reply=reply)
    except Exception as e:
        print("Error parsing response:", e)
        return ChatResponse(reply="Error: could not parse LLM response.")

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return FileResponse("chat.html")
