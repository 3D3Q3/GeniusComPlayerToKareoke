import unittest
from src.app.sync import Sync
from src.app.lyrics import Lyrics

class TestSync(unittest.TestCase):
    def setUp(self):
        self.sync = Sync()
        self.lyrics = Lyrics()

    def test_sync_lyrics_with_audio(self):
        # Sample timing data and lyrics
        timing_data = [
            (0, "First line of the song"),
            (5, "Second line of the song"),
            (10, "Third line of the song"),
        ]
        self.lyrics.set_timing_data(timing_data)

        # Simulate audio playback
        for time in range(0, 15):
            self.sync.sync_with_lyrics(time, self.lyrics)
            if time in [0, 5, 10]:
                self.assertEqual(self.lyrics.get_current_line(time), self.lyrics.get_line_at_time(time))

    def test_no_lyrics_before_start(self):
        timing_data = [
            (5, "Second line of the song"),
        ]
        self.lyrics.set_timing_data(timing_data)

        # Simulate audio playback before lyrics start
        for time in range(0, 5):
            self.sync.sync_with_lyrics(time, self.lyrics)
            self.assertIsNone(self.lyrics.get_current_line(time))

    def test_sync_with_empty_lyrics(self):
        self.lyrics.set_timing_data([])
        for time in range(0, 10):
            self.sync.sync_with_lyrics(time, self.lyrics)
            self.assertIsNone(self.lyrics.get_current_line(time))

if __name__ == '__main__':
    unittest.main()