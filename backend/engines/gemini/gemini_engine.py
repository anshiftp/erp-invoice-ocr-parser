import requests
import json
from PIL import Image
import base64

API_KEY = "AIzaSyDWXJ2IwRy0bZfOuj4-Tuo4wZayZ8YLSGg"

MODEL = "gemini-2.5-flash"

URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

def run_gemini(image_path):

    print("DEBUG: Processing image")

    with open(image_path, "rb") as f:
        image_bytes = base64.b64encode(f.read()).decode()

    prompt = """
Extract receipt data into JSON:

{
 "vendor":{"name":null,"phone":null,"address":null,"gstin":null},
 "invoice":{"number":null,"date":null},
 "items":[{"name":"","quantity":0,"unit_price":0,"total":0}],
 "amounts":{"subtotal":0,"tax":0,"grand_total":0,"currency":"INR"}
}

Return ONLY JSON.
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": image_bytes
                        }
                    }
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    print("DEBUG: Sending REST request to Gemini")

    response = requests.post(URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(response.text)
        return {}

    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    clean = text.replace("```json","").replace("```","").strip()

    return json.loads(clean)