import os
import sys
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import json
import queue
import threading
import time
from collections import deque
from resources.lib.stream_processor import AudioStreamProcessor
from resources.lib.subtitle_generator import SubtitleGenerator
from resources.lib.openai_client import OpenAIClient
from resources.lib.cache_manager import CacheManager

__addon__ = xbmcaddon.Addon()
__scriptid__ = __addon__.getAddonInfo('id')
__addon_path__ = xbmcvfs.translatePath(__addon__.getAddonInfo('path'))

class JapaneseSubtitleService(xbmc.Player):
    def __init__(self):
        super().__init__()
        self.openai_client = OpenAIClient()
        self.cache_manager = CacheManager()
        self.audio_processor = None
        self.subtitle_generator = None
        self.is_processing = False
        self.subtitle_queue = queue.Queue()
        self.subtitle_buffer = deque(maxlen=10)  # Buffer for 10 subtitle entries
        self.current_video_hash = None

    def onAVStarted(self):
        """Called when Kodi starts playing a video"""
        if self.isPlayingVideo():
            self.current_video_hash = self._get_video_hash()
            self.start_processing()

    def onPlayBackStopped(self):
        """Called when playback is stopped"""
        self.stop_processing()
        self.current_video_hash = None

    def _get_video_hash(self):
        """Generate a unique hash for the current video"""
        if self.isPlaying():
            video_info = {
                'title': self.getVideoInfoTag().getTitle(),
                'duration': self.getTotalTime(),
                'path': self.getPlayingFile()
            }
            return hash(json.dumps(video_info, sort_keys=True))
        return None

    def start_processing(self):
        if self.is_processing:
            return

        self.is_processing = True

        # Check cache first
        cached_subtitles = self.cache_manager.get_subtitles(self.current_video_hash)
        if cached_subtitles:
            xbmc.log("Found cached subtitles, loading from cache...", xbmc.LOGINFO)
            self._load_cached_subtitles(cached_subtitles)
            return

        # Initialize processors
        self.audio_processor = AudioStreamProcessor()
        self.subtitle_generator = SubtitleGenerator(
            self.openai_client,
            self.subtitle_queue,
            self.subtitle_buffer
        )

        # Start processing threads
        self.audio_thread = threading.Thread(target=self.process_audio_stream)
        self.subtitle_thread = threading.Thread(target=self.process_subtitles)
        self.display_thread = threading.Thread(target=self.display_subtitles)

        self.audio_thread.start()
        self.subtitle_thread.start()
        self.display_thread.start()

    def stop_processing(self):
        self.is_processing = False
        if self.audio_processor:
            self.audio_processor.stop()
        if self.subtitle_generator:
            self.subtitle_generator.stop()

        # Cache subtitles before stopping
        if self.subtitle_buffer and self.current_video_hash:
            self.cache_manager.save_subtitles(
                self.current_video_hash,
                list(self.subtitle_buffer)
            )

    def process_audio_stream(self):
        """Process audio stream in chunks"""
        chunk_buffer = []
        while self.is_processing:
            try:
                audio_chunk = self.audio_processor.get_next_chunk()
                if audio_chunk:
                    chunk_buffer.append(audio_chunk)

                    # Process when we have enough audio data
                    if len(chunk_buffer) >= 3:  # ~300ms of audio
                        combined_chunk = b''.join(chunk_buffer)
                        transcription = self.openai_client.transcribe_audio(combined_chunk)
                        if transcription:
                            self.subtitle_queue.put(transcription)
                        chunk_buffer = []

            except Exception as e:
                xbmc.log(f"Error processing audio: {str(e)}", xbmc.LOGERROR)
                time.sleep(0.1)

    def process_subtitles(self):
        """Process subtitles and add them to buffer"""
        while self.is_processing:
            try:
                subtitle = self.subtitle_queue.get(timeout=1)
                if subtitle:
                    processed_subtitle = self.subtitle_generator.process_transcript(subtitle)
                    self.subtitle_buffer.append(processed_subtitle)
            except queue.Empty:
                continue
            except Exception as e:
                xbmc.log(f"Error processing subtitles: {str(e)}", xbmc.LOGERROR)
                time.sleep(0.1)

    def display_subtitles(self):
        """Display subtitles from buffer"""
        last_subtitle = None
        while self.is_processing:
            try:
                if self.subtitle_buffer:
                    current_subtitle = self.subtitle_buffer[-1]
                    if current_subtitle != last_subtitle:
                        self.show_subtitle(current_subtitle)
                        last_subtitle = current_subtitle
                time.sleep(0.1)
            except Exception as e:
                xbmc.log(f"Error displaying subtitles: {str(e)}", xbmc.LOGERROR)
                time.sleep(0.1)

    def _load_cached_subtitles(self, cached_subtitles):
        """Load subtitles from cache and display them"""
        self.subtitle_buffer.extend(cached_subtitles)
        threading.Thread(target=self.display_subtitles).start()

    def show_subtitle(self, subtitle):
        """Display the subtitle on screen"""
        text = (
            f"{subtitle['japanese']}\n"
            f"{subtitle['romaji']}\n"
            f"{subtitle['translation']}"
        )
        self.showSubtitles(text)