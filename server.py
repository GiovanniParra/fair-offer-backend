import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import json
import os # <--- Important for the Cloud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This gets the key from Render's settings
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    text: str

@app.post("/generate")
def generate_reply(request: ChatRequest):
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # --- RESTORED: THE CHARMING PERSONALITY PROMPT ---
    prompt = f"""
    Context: Negotiation for a used item on Facebook Marketplace.
    Seller said: "{request.text}"
    
    Return a JSON object with 3 reply options (keys: quick, lowball, polite).
    
    1. "quick" (The Charming Cash): Be upbeat, friendly, and emphasize the value of FAST CASH. Make it sound like an easy, stress-free win for them.
       Example: "hey! honestly i love this. i can swing by with cash today and take it off your hands. would you do..."
       
    2. "lowball" (The Logic): Do not just give a number. Explain WHY (condition, market value, clearing space). Make them feel like you are doing them a favor by picking it up now.
       Example: "hey, cool find. honestly these usually sit for a while at this price. since i can pick it up rn and save you the hassle, would you take..."
       
    3. "polite" (The Friendly): Very respectful, genuinely interested, asking for wiggle room.
       Example: "hey there! really interested in this. is the price firm or do you have any wiggle room for a student?"
    
    Output JSON only. Keys must be lowercase strings.
    """
    
    try:
        response = model.generate_content(prompt)
        clean = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        return {"quick": "Error generating", "lowball": "Try again", "polite": "Check server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
