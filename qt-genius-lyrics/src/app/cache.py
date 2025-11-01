import os
import json
from typing import Optional


class Cache:
    def __init__(self, cache_dir: Optional[str] = None):
        # Default cache dir: <repo>/qt-genius-lyrics/data/cache
        if cache_dir is None:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            cache_dir = os.path.join(repo_root, 'data', 'cache')

        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_file_path(self, key: str) -> str:
        safe_key = self._sanitize_key(key)
        return os.path.join(self.cache_dir, f"{safe_key}.json")

    def _sanitize_key(self, key: str) -> str:
        # Basic sanitization: replace spaces and slashes
        return str(key).strip().replace(' ', '_').replace('/', '_')

    # Primary read/write helpers (existing names)
    def load_cache(self, key: str):
        try:
            with open(self.get_cache_file_path(key), 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_cache(self, key: str, data) -> None:
        with open(self.get_cache_file_path(key), 'w', encoding='utf-8') as f:
            json.dump(data, f)
        self._evict_if_needed()

    def clear_cache(self, key: str) -> None:
        try:
            os.remove(self.get_cache_file_path(key))
        except FileNotFoundError:
            pass

    def clear_all_cache(self) -> None:
        for filename in os.listdir(self.cache_dir):
            file_path = os.path.join(self.cache_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    # Compatibility wrappers used in tests and UI
    def store(self, key: str, data) -> None:
        """Alias used by tests: store(key, value) -> save_cache(key, value)"""
        self.save_cache(key, data)

    def retrieve(self, key: str):
        """Alias used by tests: retrieve(key) -> load_cache(key)"""
        return self.load_cache(key)

    def clear(self) -> None:
        """Alias used by tests to clear all cache files."""
        self.clear_all_cache()

    # Helpers used by the application UI
    def get_song_data(self, query: str):
        return self.load_cache(query)

    def save_song_data(self, query: str, data) -> None:
        self.save_cache(query, data)

    # Simple eviction policy: keep at most 10 files; remove oldest by mtime
    def _evict_if_needed(self) -> None:
        try:
            files = [os.path.join(self.cache_dir, f) for f in os.listdir(self.cache_dir) if os.path.isfile(os.path.join(self.cache_dir, f))]
            max_files = 10
            if len(files) <= max_files:
                return

            # Sort by modification time, tie-break by filename to get a deterministic
            # eviction order when files are created very close in time (tests create
            # files in a tight loop). This ensures `song_0` will be evicted first in
            # the unit test scenario.
            files.sort(key=lambda p: (os.path.getmtime(p), p))
            while len(files) > max_files:
                to_remove = files.pop(0)
                try:
                    os.remove(to_remove)
                except Exception:
                    pass
        except Exception:
            # Best-effort eviction; don't crash the app for eviction errors
            pass