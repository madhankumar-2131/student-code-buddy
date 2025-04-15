from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

app = Flask(__name__)

# Get Hugging Face token from .env
HF_TOKEN = os.getenv("HF_TOKEN")

# Use a small, free-tier compatible model
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_code_from_hf(prompt):
    payload = {"inputs": prompt.strip()}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        generated = response.json()[0]["generated_text"]
        return generated.replace(prompt.strip(), "").strip()
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    code = get_code_from_hf(prompt)
    return jsonify({"code": code})

if __name__ == "__main__":
    app.run(debug=True)
