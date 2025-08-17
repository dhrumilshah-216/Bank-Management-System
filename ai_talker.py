import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("API_KEY")  
MODEL = os.getenv("MODEL") 
def ask_ai(text):
    url = os.getenv("url")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": os.getenv("prompt")
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "max_tokens": 500
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    reply = response.json()

    return reply["choices"][0]["message"]["content"].strip()
