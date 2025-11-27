import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# This lets Chrome talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 PASTE YOUR KEY BELOW
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    text: str

@app.post("/generate")
def generate_reply(request: ChatRequest):
    model = genai.GenerativeModel("gemini-2.5-flash") # Or "gemini-pro"
    
    prompt = f"""
    Context: Negotiation for a used item on Facebook Marketplace.
    Seller said: "{request.text}"
    
    Return a JSON object with 3 keys: "quick", "lowball", "polite".
    Values must be short, casual, lowercase messages.
    """
    
    try:
        response = model.generate_content(prompt)
        clean = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        return {"quick": "error", "lowball": "error", "polite": "check server console"}

if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
