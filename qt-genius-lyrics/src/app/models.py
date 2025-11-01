class Song:
    def __init__(self, title, artist, lyrics_data):
        self.title = title
        self.artist = artist
        self.lyrics_data = lyrics_data

class LyricsData:
    def __init__(self, lyrics, timing):
        self.lyrics = lyrics
        self.timing = timing

    def get_lyric_at_time(self, time):
        # Logic to retrieve the lyric corresponding to the given time
        pass

    def get_all_lyrics(self):
        return self.lyrics

    def get_timing(self):
        return self.timing