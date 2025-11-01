from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from src.app.genius_client import GeniusClient
from src.app.lyrics import Lyrics
from src.app.player import Player
from src.app.cache import Cache

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genius Lyrics Finder")
        self.setGeometry(100, 100, 600, 400)

        self.cache = Cache()
        self.genius_client = GeniusClient()
        self.player = Player()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.search_label = QLabel("Search for a song or artist:")
        layout.addWidget(self.search_label)

        self.search_box = QLineEdit(self)
        layout.addWidget(self.search_box)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_song)
        layout.addWidget(self.search_button)

        self.lyrics_display = QTextEdit(self)
        self.lyrics_display.setReadOnly(True)
        layout.addWidget(self.lyrics_display)

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())