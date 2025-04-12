"""Cache management utilities."""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from ..config import CACHE_DIR

def get_file_hash(file_path: Path) -> str:
    """Generate a hash of the file content for caching."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def save_to_cache(cache_data: dict, file_hash: str) -> None:
    """Save data to cache file."""
    cache_file = CACHE_DIR / f"{file_hash}.json"
    cache_data['timestamp'] = datetime.now().isoformat()
    cache_file.write_text(json.dumps(cache_data, indent=2))

def get_from_cache(file_path: Path) -> tuple[Path | None, dict | None]:
    """Get cached data if it exists.
    
    Returns:
        tuple: (transcript_path, cache_data) or (None, None) if not found
    """
    file_hash = get_file_hash(file_path)
    cache_file = CACHE_DIR / f"{file_hash}.json"
    
    if cache_file.exists():
        print("Found cached transcript...")
        cache_data = json.loads(cache_file.read_text())
        transcript_path = Path(cache_data['transcript_path'])
        if transcript_path.exists():
            print(f"Using cached transcript: {transcript_path}")
            return transcript_path, cache_data
    return None, None
