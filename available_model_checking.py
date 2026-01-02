import os
import requests
from dotenv import load_dotenv

import os
load_dotenv()

print(os.getenv("GEMINI_API_KEY"))
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY in environment variables")

url = "https://generativelanguage.googleapis.com/v1beta/models"
headers = {
    "x-goog-api-key": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Error:", response.status_code, response.text)
else:
    data = response.json()
    models_list = data.get("models", [])
    if not models_list:
        print("No models returned — maybe key has no access?")
    for model in models_list:
        name = model.get("name")
        methods = model.get("supportedGenerationMethods", [])
        print(name, "→", methods)
