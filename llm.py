import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def generate_response(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt" : prompt,
        "stream" : False,
        "options": {
            "num_predict":150
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL, 
            headers={"Content-Type": "application/json"},
            data = json.dumps(payload), 
            timeout=1000
        )

        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    
    except Exception as e:
        print("LLM Error:", e)
        return "Sorry, I'm having trouble generating a response right now."
    

