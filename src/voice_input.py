"""
NeuroVault Voice Input
Speech-to-text functionality using Google Speech Recognition
"""

import speech_recognition as sr


def listen_and_transcribe(timeout=5, phrase_time_limit=10):
    """
    Listen to microphone and transcribe speech to text
    
    Args:
        timeout: Max seconds to wait for speech to start
        phrase_time_limit: Max seconds for the entire phrase
    
    Returns:
        str: Transcribed text, or None if failed
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("🎤 Listening...")
            audio = recognizer.listen(
                source, 
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
            
            print("🔄 Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"✅ Transcribed: {text}")
            return text
            
    except sr.WaitTimeoutError:
        print("⏱️ No speech detected (timeout)")
        return None
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return None
    except OSError as e:
        print(f"❌ Microphone error: {e}")
        return None
    except Exception as e:
        print(f"❌ Voice input error: {e}")
        return None


def check_microphone_available():
    """Check if a microphone is available"""
    try:
        with sr.Microphone() as source:
            return True
    except OSError:
        return False
    except Exception:
        return False
