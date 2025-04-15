from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Hugging Face token
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("⚠️ Warning: HF_TOKEN not found in environment!")

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_code_from_hf(prompt):
    payload = {"inputs": f"# {prompt.strip()}"}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            generated = data[0]["generated_text"]
            return generated.replace(f"# {prompt.strip()}", "").strip()
        else:
            return "Error: Unexpected response format from Hugging Face API."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: {http_err}"
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt.strip():
        return jsonify({"code": "❌ Prompt is empty. Please enter a valid question."})
    code = get_code_from_hf(prompt)
    return jsonify({"code": code})

if __name__ == "__main__":
    app.run(debug=True)
