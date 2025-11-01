import unittest
from src.app.cache import Cache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache()

    def test_store_and_retrieve(self):
        key = "test_song"
        value = {"lyrics": "Test lyrics", "timing": [0, 10, 20]}
        self.cache.store(key, value)
        retrieved_value = self.cache.retrieve(key)
        self.assertEqual(retrieved_value, value)

    def test_retrieve_non_existent(self):
        key = "non_existent_song"
        retrieved_value = self.cache.retrieve(key)
        self.assertIsNone(retrieved_value)

    def test_cache_eviction(self):
        for i in range(10):
            self.cache.store(f"song_{i}", {"lyrics": f"Lyrics for song {i}", "timing": [0, 10]})
        self.cache.store("song_10", {"lyrics": "Lyrics for song 10", "timing": [0, 10]})
        self.assertIsNone(self.cache.retrieve("song_0"))

    def tearDown(self):
        self.cache.clear()

if __name__ == '__main__':
    unittest.main()