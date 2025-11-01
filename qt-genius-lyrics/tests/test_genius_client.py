import unittest
from src.app.genius_client import GeniusClient

class TestGeniusClient(unittest.TestCase):

    def setUp(self):
        self.client = GeniusClient(api_token='your_api_token_here')

    def test_search_song(self):
        song_title = "Shape of You"
        artist_name = "Ed Sheeran"
        result = self.client.search_song(song_title, artist_name)
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('artist', result)

    def test_get_lyrics(self):
        song_id = 123456  # Replace with a valid song ID
        lyrics = self.client.get_lyrics(song_id)
        self.assertIsNotNone(lyrics)
        self.assertIn('lyrics', lyrics)

    def test_handle_api_error(self):
        with self.assertRaises(Exception):
            self.client.search_song("", "")  # Invalid search parameters

if __name__ == '__main__':
    unittest.main()