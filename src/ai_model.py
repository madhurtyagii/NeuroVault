import requests
import json
import os
from pathlib import Path

# Load API key from .env file
def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()

# Groq API configuration (fast & free)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

def get_ai_response(prompt, max_tokens=500):
    """
    Get AI response from Groq API (or local Ollama fallback)
    
    Args:
        prompt: The prompt to send to AI
        max_tokens: Maximum response length
    
    Returns:
        AI response text
    """
    
    # Try Groq first (fast, cloud-based) if API key is set
    if GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            print(f"🔄 Calling Groq API with model: {MODEL_NAME}")
            
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Groq API success!")
                return data["choices"][0]["message"]["content"].strip()
            else:
                print(f"❌ Groq API error: {response.status_code}")
                print(f"Response: {response.text}")
        
        except Exception as e:
            print(f"❌ Groq exception: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ Groq API key not found in .env file")
    
    # Fallback to local Ollama
    try:
        print("🔄 Using local Ollama...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": max_tokens
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["response"].strip()
    
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return "❌ AI unavailable. Add GROQ_API_KEY to .env file or start Ollama."
    
    return "❌ Could not generate response. Check your AI setup."

def test_ai_connection():
    """Test if AI is available"""
    try:
        response = get_ai_response("Say 'Hello!' if you can hear me.", max_tokens=50)
        return "Hello" in response or "hello" in response
    except:
        return False
