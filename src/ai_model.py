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

# Available models configuration
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

OLLAMA_MODELS = [
    "llama3.2",
    "mistral",
    "codellama",
    "llama2"
]

# Current model state
current_model = "llama-3.3-70b-versatile"
current_provider = "groq"  # "groq" or "ollama"


def set_model(model_name):
    """Set the current AI model"""
    global current_model, current_provider
    current_model = model_name
    # Determine provider based on model name
    if model_name in GROQ_MODELS:
        current_provider = "groq"
    else:
        current_provider = "ollama"
    print(f"🔄 Switched to model: {model_name} (provider: {current_provider})")


def get_available_models():
    """Get list of available models"""
    models = []
    # Add Groq models (always available if API key set)
    if GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
        models.extend(GROQ_MODELS)
    # Add Ollama models
    models.extend(OLLAMA_MODELS)
    return models


def get_ai_response_stream(prompt, max_tokens=500):
    """
    Stream AI response from Groq API or Ollama
    
    Yields:
        str: Chunks of the response text
    """
    global current_model, current_provider
    
    # Use Groq if provider is groq and API key is set
    if current_provider == "groq" and GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": current_model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": True
            }
            
            print(f"🔄 Streaming from Groq API with model: {current_model}")
            
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=60,
                stream=True
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode('utf-8')
                        if line_text.startswith('data: '):
                            data_str = line_text[6:]
                            if data_str.strip() == '[DONE]':
                                break
                            try:
                                data = json.loads(data_str)
                                delta = data.get('choices', [{}])[0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue
                print("✅ Groq streaming complete!")
                return
            else:
                print(f"❌ Groq API error: {response.status_code}")
        except Exception as e:
            print(f"❌ Groq streaming exception: {e}")
    
    # Fallback to Ollama streaming
    try:
        ollama_model = current_model if current_provider == "ollama" else "llama3.2"
        print(f"🔄 Streaming from Ollama with model: {ollama_model}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "num_predict": max_tokens
                }
            },
            timeout=120,
            stream=True
        )
        
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        token = data.get('response', '')
                        if token:
                            yield token
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
            print("✅ Ollama streaming complete!")
            return
    except Exception as e:
        print(f"❌ Ollama streaming error: {e}")
    
    yield "❌ AI unavailable. Add GROQ_API_KEY to .env file or start Ollama."


def get_ai_response(prompt, max_tokens=500):
    """
    Get AI response from Groq API (or local Ollama fallback)
    
    Args:
        prompt: The prompt to send to AI
        max_tokens: Maximum response length
    
    Returns:
        AI response text
    """
    global current_model, current_provider
    
    # Try Groq first if provider is groq and API key is set
    if current_provider == "groq" and GROQ_API_KEY and GROQ_API_KEY.startswith("gsk_"):
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": current_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            print(f"🔄 Calling Groq API with model: {current_model}")
            
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
    elif current_provider == "groq":
        print("⚠️ Groq API key not found in .env file")
    
    # Fallback to local Ollama
    try:
        ollama_model = current_model if current_provider == "ollama" else "llama3.2"
        print(f"🔄 Using local Ollama with model: {ollama_model}")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": ollama_model,
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
