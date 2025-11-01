# qt-genius-lyrics

## Overview
The Qt Genius Lyrics application is a Python-based desktop application that allows users to search for songs and artists, retrieve song data from Genius.com, and display synchronized lyrics along with audio playback. The application features a clean and minimal user interface built using PyQt.

## Features
- User search interface for song and artist name lookup.
- Retrieves song data and lyrics from Genius.com.
- Loads corresponding music videos within the application window.
- Synchronizes audio playback with lyrics, displaying them in real-time.
- Caches song data for faster access and improved performance.
- Saves local versions of lyrics and video timing in a space-efficient manner.

## Project Structure
```
qt-genius-lyrics
├── src
│   ├── main.py                # Entry point of the application
│   ├── app                    # Application logic
│   │   ├── __init__.py
│   │   ├── gui.py             # Main GUI logic
│   │   ├── main_window.py      # Main application window
│   │   ├── player.py          # Audio playback management
│   │   ├── genius_client.py    # API requests to Genius.com
│   │   ├── lyrics.py          # Lyrics management
│   │   ├── sync.py            # Synchronization logic
│   │   ├── cache.py           # Caching mechanisms
│   │   └── models.py          # Data models
│   ├── ui                     # UI files
│   │   └── main_window.ui      # Qt Designer file for UI layout
│   └── resources              # Resource files
│       └── qrc_resources.py    # Resource definitions
├── data                       # Data storage
│   ├── cache                  # Cached lyrics and metadata
│   └── metadata               # Metadata files
├── tests                      # Unit tests
│   ├── test_genius_client.py   # Tests for GeniusClient
│   ├── test_cache.py           # Tests for caching mechanisms
│   └── test_sync.py            # Tests for synchronization logic
├── requirements.txt           # Project dependencies
├── pyproject.toml             # Project configuration
├── .gitignore                 # Git ignore file
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd qt-genius-lyrics
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.