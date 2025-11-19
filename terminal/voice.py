import os
import threading
import time
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

class VoiceManager:
    def __init__(self):
        self.enabled = False
        self.recognizer = sr.Recognizer() if sr else None
        self.engine = None
        self.is_speaking = False
        
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 170)  # Slightly faster than default
                self.engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"Voice output init failed: {e}")

    def is_available(self) -> bool:
        return sr is not None and pyttsx3 is not None

    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice input and return text."""
        if not self.enabled or not self.recognizer:
            return None
            
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio)
            print(f"🎤 You said: {text}")
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("🎤 Could not understand audio")
            return None
        except Exception as e:
            print(f"🎤 Error: {e}")
            return None

    def speak(self, text: str):
        """Speak the provided text in a separate thread."""
        if not self.enabled or not self.engine:
            return

        # Don't speak code blocks or very long text entirely
        if "```" in text:
            text = "I have generated some code. Please check the terminal."
        
        if len(text) > 500:
            text = text[:500] + "... (speech truncated)"

        def _speak_thread():
            self.is_speaking = True
            try:
                # Re-init engine for thread safety if needed, but pyttsx3 usually handles it
                # or we use the existing engine loop
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False

        threading.Thread(target=_speak_thread, daemon=True).start()
