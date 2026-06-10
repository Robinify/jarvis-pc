"""
Voice Input/Output Handling for macOS
"""

import subprocess
import logging
from typing import Dict, Optional

try:
    import speech_recognition as sr
except ImportError:
    sr = None

logger = logging.getLogger(__name__)


class VoiceHandler:
    """Handle voice input and output on macOS"""
    
    def __init__(self, config: Dict):
        """Initialize voice handler"""
        self.enabled = config.get("enabled", True)
        self.input_enabled = config.get("input_enabled", True)
        self.output_enabled = config.get("output_enabled", True)
        self.rate = config.get("rate", 200)
        self.volume = config.get("volume", 1.0)
        self.engine = config.get("engine", "say")
        
        # Initialize speech recognizer if input is enabled
        if self.input_enabled and sr is not None:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        else:
            self.recognizer = None
            self.microphone = None
        
        logger.info("Voice handler initialized")
    
    def recognize_speech(self) -> Optional[str]:
        """Recognize speech from microphone"""
        if not self.input_enabled or self.recognizer is None:
            return None
        
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for speech with timeout
                audio = self.recognizer.listen(source, timeout=10)
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            return None
    
    def speak(self, text: str) -> bool:
        """Speak text using macOS text-to-speech"""
        if not self.output_enabled:
            return False
        
        try:
            # Use macOS 'say' command for text-to-speech
            rate_arg = int(self.rate)
            volume_arg = int(self.volume * 100)
            
            cmd = [
                self.engine,
                "-r", str(rate_arg),
                "-v", "Samantha",  # Quality voice on macOS
                text
            ]
            
            # Execute say command
            subprocess.run(
                cmd,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            return True
        
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return False
