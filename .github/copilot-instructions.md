## Purpose

This file gives focused, repo-specific instructions for AI coding agents working on GeniusComPlayerToKareoke (the Qt Genius Lyrics app). Use these notes to be productive quickly: where to look, how components interact, and concrete examples to follow.

## Big-picture architecture (quick)

- Top-level app: `qt-genius-lyrics/src/main.py` — creates a PyQt5 QApplication and `MainWindow`.
- UI / entry: `qt-genius-lyrics/src/app/main_window.py` and `ui/main_window.ui` — search UI wiring here.
- Core services:
  - `app/genius_client.py` — communicates with the Genius API (search, fetch song/lyrics).
  - `app/cache.py` — file-based JSON cache under `qt-genius-lyrics/data/cache`.
  - `app/lyrics.py` and `app/models.py` — lyric formatting, timing and model classes.
  - `app/player.py` and `app/sync.py` — audio playback and lyrics synchronization (QMediaPlayer + QTimer).

Dataflow summary: GUI triggers search -> GeniusClient fetches song metadata/lyrics -> data is cached (Cache) -> Player loads audio -> Sync polls QMediaPlayer to display timed lines from Lyrics.

## Key patterns & conventions to follow

- PyQt5 idioms: use `QApplication`, `QMainWindow`, `QTimer`, and `QMediaPlayer` (see `sync.py`). Changes to UI typically touch `main_window.py` and `ui/main_window.ui`.
- File-based caching: store JSON in `data/cache` using keys derived from song/artist (see `cache.py`). Keep cache read/write simple and resilient to missing files.
- API token handling: `GeniusClient` expects a token (constructors vary across files/tests). Favor explicit parameter `api_token` or reading from an env var named `GENIUS_API_TOKEN` when adding new code.
- Naming inconsistencies exist: method names and parameter names differ across modules and tests (e.g., `store()` vs `save_cache()` or `api_token` vs `access_token`). When editing, search for all variants and update usages consistently.

## How to run & test locally

- Install deps (from repo root):
  - pip install -r qt-genius-lyrics/requirements.txt
- Run the app:
  - python qt-genius-lyrics/src/main.py
- Run tests (unit tests live in `qt-genius-lyrics/tests`):
  - python -m unittest discover -s qt-genius-lyrics/tests
  - or: pytest -q qt-genius-lyrics/tests

If tests fail due to missing API tokens or network calls, mock `GeniusClient` or set `GENIUS_API_TOKEN` for integration-style tests.

## Integration points and gotchas

- Genius.com API: `app/genius_client.py` — network calls assume token-based auth. Tests show constructing `GeniusClient(api_token=...)`.
- Audio/video: the app expects to load audio/video URLs returned by Genius metadata; multimedia behavior depends on host OS codecs and PyQt5 multimedia support.
- Duplicate/parallel source trees: there is a `qt-genius-lyrics-1/` copy. Prefer working in `qt-genius-lyrics/` unless instructed otherwise.
- Inconsistent APIs: tests and modules use different method names and signatures. Before refactoring, run a repo-wide search for method names (e.g., `search_song`, `fetch_song_data`, `get_lyrics`, `store`, `save_cache`) and ensure you update all callers.

## Small examples to copy/paste

- Entry point: `qt-genius-lyrics/src/main.py`
  - Creates QApplication and shows `MainWindow`.
- Fetch & cache pattern (example in `main_window.py`):
  - song_data = cache.get_song_data(query) or genius_client.fetch_song_data(query)
  - cache.save_song_data(query, song_data)
  - lyrics = Lyrics(song_data['lyrics'])

## When editing code, focus on these tests

- `qt-genius-lyrics/tests/test_genius_client.py` — validates the GeniusClient behavior.
- `qt-genius-lyrics/tests/test_cache.py` — shows expected cache API (store/retrieve/clear).
- `qt-genius-lyrics/tests/test_sync.py` — demonstrates sync behavior and expected lyrics timing API.

## Quick troubleshooting tips

- If GUI doesn't show audio/video: verify PyQt5 multimedia installed and that `QMediaPlayer` can access codecs on the host.
- If tests import failure occurs: run tests with cwd set to `qt-genius-lyrics/` or ensure `PYTHONPATH` includes `qt-genius-lyrics/src`.
- If APIs appear to mismatch: run a repo-wide grep for the symbol and align callers before changing a signature.

## Ask me if any details are missing

If you want more examples (common refactors, preferred token handling, or an agreed contract for Cache/GeniusClient APIs), tell me which area to standardize and I'll update this file with concrete recipes.
