import requests, json
from apikey import api_key 

headers = {"Authorization": f"Bearer {api_key}"}

data = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "system", "content": "You are a non friendly,un humoured,non challant,very aggressive multilingual chatbot."},
        {"role": "user", "content": "hello how are you can u tell me the steps to build multingual ai chatbot"}
    ]
}

res = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers=headers,
    json=data
)
# Safely extract message if it exists
if "choices" in res.json():
    print("\nAI Reply:", res.json()["choices"][0]["message"]["content"])
else:
    print("\nError:", res.json().get("error", {}).get("message", "Unknown error"))
