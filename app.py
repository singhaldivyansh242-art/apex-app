from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("NVIDIA_API_KEY")
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_apex():
    data = request.json
    user_message = data.get("message", "")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are Apex, a highly advanced and capable AI assistant. Speak concisely, intelligently, and professionally."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 256
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Apex System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

