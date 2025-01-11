from collections import deque
import threading
import time

class SubtitleGenerator:
    def __init__(self, openai_client, queue, buffer):
        self.openai_client = openai_client
        self.queue = queue
        self.buffer = buffer
        self.is_running = True
        self.last_processed = {}
        self.processing_lock = threading.Lock()

    def process_transcript(self, transcript):
        """Process transcript into three-line format using GPT-4"""
        with self.processing_lock:
            # Check if we've recently processed this text
            if transcript in self.last_processed:
                return self.last_processed[transcript]

            prompt = f"""
            For the Japanese text: {transcript}
            Provide three lines:
            1. The original Japanese text
            2. The romaji pronunciation in parentheses
            3. Word-by-word English translation in square brackets
            Format exactly as shown in the example:
            私は学生です。
            (Watashi wa gakusei desu.)
            [I + TOPIC + student + BE]
            """

            response = self.openai_client.get_gpt4_response(prompt)
            result = self.parse_gpt4_response(response)

            # Cache the result
            self.last_processed[transcript] = result
            if len(self.last_processed) > 100:  # Limit cache size
                self.last_processed.pop(next(iter(self.last_processed)))

            return result

    def parse_gpt4_response(self, response):
        """Parse GPT-4 response into structured format"""
        try:
            lines = response.strip().split('\n')
            return {
                'japanese': lines[0].strip(),
                'romaji': lines[1].strip(),
                'translation': lines[2].strip()
            }
        except Exception as e:
            xbmc.log(f"Error parsing GPT-4 response: {str(e)}", xbmc.LOGERROR)
            return None

    def stop(self):
        self.is_running = False