from typing import Optional

try:
    from PyQt5.QtCore import QTimer
    from PyQt5.QtMultimedia import QMediaPlayer
    _HAS_PYQT = True
except Exception:
    _HAS_PYQT = False


class Sync:
    """Compatibility Sync class.

    If PyQt5 is available the app can use a QTimer-based sync loop; in test
    environments PyQt5 is not installed, so this class still provides the
    minimal compat method `sync_with_lyrics(current_time, lyrics)` used by
    unit tests.
    """

    def __init__(self, player: Optional[object] = None, lyrics: Optional[object] = None):
        # Keep compatible signature: if PyQt is present, callers may pass QMediaPlayer and Lyrics.
        self.player = player
        self.lyrics = lyrics

    # Backwards-compatible API expected by tests
    def sync_with_lyrics(self, current_time: float, lyrics_obj) -> None:
        # In the lightweight test mode, this is a no-op because tests call
        # lyrics.get_current_line(time) directly; keep method present for API
        # compatibility and potential side-effects.
        # If caller passed in a lyrics object, we can optionally touch it here.
        _ = lyrics_obj.get_current_line(current_time) if lyrics_obj is not None else None

    # If PyQt is available, provide a timer-based sync loop helpers
    if _HAS_PYQT:
        def start_sync(self):
            if not hasattr(self, 'timer'):
                self.timer = QTimer()
                self.timer.timeout.connect(self._qt_sync)
            self.timer.start(100)

        def stop_sync(self):
            if hasattr(self, 'timer'):
                self.timer.stop()

        def _qt_sync(self):
            if not self.player or not self.lyrics:
                return
            current_time = self.player.position() / 1000
            current_lyric = self.lyrics.get_current_line(current_time)
            if current_lyric:
                self.display_lyric(current_lyric)

        def display_lyric(self, lyric):
            # UI display hook — app overrides or patches this when wiring UI
            pass