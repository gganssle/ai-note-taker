"""Configuration settings for the voice memo analyzer."""

from pathlib import Path

# Base directories
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
MP3_DIR = DATA_DIR / "mp3_conversions"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"
CACHE_DIR = DATA_DIR / "cache"
RESULTS_DIR = DATA_DIR / "results"

# Ensure directories exist
REQUIRED_DIRS = [DATA_DIR, MP3_DIR, TRANSCRIPT_DIR, CACHE_DIR, RESULTS_DIR]
for dir_path in REQUIRED_DIRS:
    dir_path.mkdir(exist_ok=True)
