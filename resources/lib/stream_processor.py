import numpy as np
import pyaudio
import wave
from threading import Lock
import time

class AudioStreamProcessor:
    def __init__(self):
        self.chunk_size = 4096
        self.sample_rate = 16000
        self.is_running = True
        self.lock = Lock()
        self.buffer_size = 10  # Buffer size in chunks

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.audio_callback
        )

        self.audio_buffer = deque(maxlen=self.buffer_size)

    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.is_running:
            with self.lock:
                self.audio_buffer.append(in_data)
        return (in_data, pyaudio.paContinue)

    def get_next_chunk(self):
        """Get the next audio chunk for processing"""
        with self.lock:
            if len(self.audio_buffer) > 0:
                return self.audio_buffer.popleft()
        time.sleep(0.01)  # Small delay to prevent busy waiting
        return None

    def stop(self):
        self.is_running = False
        time.sleep(0.1)  # Allow final callbacks to complete
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()