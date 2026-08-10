from flask import Flask, request, jsonify, render_template
import requests
import os
import base64

app = Flask(__name__)

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_apex():
    data = request.json
    user_message = data.get("message", "")
    is_voice = data.get("isVoice", False)
    
    nv_headers = {"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"}
    nv_payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [
            {"role": "system", "content": "You are Apex, a highly advanced AI assistant. Speak concisely, naturally, and professionally, as if speaking out loud."},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 256
    }
    
    try:
        nv_response = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=nv_headers, json=nv_payload)
        nv_response.raise_for_status() 
        reply_text = nv_response.json()["choices"][0]["message"]["content"]
        
        audio_base64 = None
        
        if is_voice and ELEVENLABS_API_KEY:
            el_url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
            el_headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
            el_payload = {"text": reply_text, "model_id": "eleven_turbo_v2"}
            
            el_response = requests.post(el_url, headers=el_headers, json=el_payload)
            if el_response.status_code == 200:
                audio_base64 = base64.b64encode(el_response.content).decode('utf-8')

        return jsonify({"reply": reply_text, "audio": audio_base64})
        
    except Exception as e:
        return jsonify({"reply": f"Apex System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

