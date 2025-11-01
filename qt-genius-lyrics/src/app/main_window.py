from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from .genius_client import GeniusClient
from .lyrics import Lyrics
from .player import Player
from .cache import Cache

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genius Lyrics Finder")
        self.setGeometry(100, 100, 800, 600)

        self.cache = Cache()
        self.genius_client = GeniusClient()
        self.player = Player()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Enter song title and artist...")
        layout.addWidget(self.search_box)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_song)
        layout.addWidget(self.search_button)

        self.lyrics_display = QTextEdit(self)
        self.lyrics_display.setReadOnly(True)
        layout.addWidget(self.lyrics_display)

        self.video_label = QLabel("Video will be displayed here", self)
        layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_song(self):
        query = self.search_box.text()
        if query:
            song_data = self.cache.get_song_data(query)
            if not song_data:
                song_data = self.genius_client.fetch_song_data(query)
                self.cache.save_song_data(query, song_data)

            lyrics = Lyrics(song_data['lyrics'])
            self.lyrics_display.setPlainText(lyrics.get_formatted_lyrics())
            self.player.load_audio(song_data['audio_url'])
            self.player.play()

            # Load video logic would go here
            self.video_label.setText("Video loaded for: " + song_data['title'])