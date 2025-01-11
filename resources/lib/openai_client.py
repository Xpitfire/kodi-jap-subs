import os
import requests
import json
import tempfile
import time
from functools import lru_cache
import xbmcaddon
import xbmc

class OpenAIClient:
    def __init__(self):
        self.api_key = xbmcaddon.Addon().getSetting("openai_api_key")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.request_cooldown = 0.1  # 100ms between requests
        self.last_request_time = 0

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_cooldown:
            time.sleep(self.request_cooldown - time_since_last)
        self.last_request_time = time.time()

    @lru_cache(maxsize=1000)
    def transcribe_audio(self, audio_data):
        """Send audio chunk to Whisper API with caching"""
        self._rate_limit()

        # Save audio chunk to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name

        try:
            with open(temp_path, 'rb') as audio_file:
                response = requests.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files={"file": audio_file},
                    data={
                        "model": "whisper-1",
                        "language": "ja",
                        "response_format": "json"
                    }
                )
            os.unlink(temp_path)
            return response.json()['text'] if response.ok else None
        except Exception as e:
            xbmc.log(f"Error in transcription: {str(e)}", xbmc.LOGERROR)
            return None

    @lru_cache(maxsize=1000)
    def get_gpt4_response(self, prompt):
        """Get GPT-4 response for translation and romanization with caching"""
        self._rate_limit()

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=self.headers,
                json={
                    "model": "gpt-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3
                }
            )
            if response.ok:
                return response.json()['choices'][0]['message']['content']
            else:
                xbmc.log(f"GPT-4 API error: {response.status_code}", xbmc.LOGERROR)
                return None
        except Exception as e:
            xbmc.log(f"Error in GPT-4 request: {str(e)}", xbmc.LOGERROR)
            return None

    def clear_cache(self):
        """Clear the function caches"""
        self.transcribe_audio.cache_clear()
        self.get_gpt4_response.cache_clear()