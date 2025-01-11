import os
import json
from diskcache import Cache
import xbmcvfs
import xbmcaddon

class CacheManager:
    def __init__(self):
        addon = xbmcaddon.Addon()
        cache_dir = xbmcvfs.translatePath(
            os.path.join(addon.getAddonInfo('profile'), 'cache')
        )
        self.cache = Cache(cache_dir)
        self.cache_duration = 60 * 60 * 24 * 7  # 1 week

    def get_subtitles(self, video_hash):
        """Get cached subtitles for a video"""
        if video_hash in self.cache:
            return self.cache[video_hash]
        return None

    def save_subtitles(self, video_hash, subtitles):
        """Save subtitles to cache"""
        self.cache.set(video_hash, subtitles, expire=self.cache_duration)

    def clear_cache(self):
        """Clear the entire cache"""
        self.cache.clear()