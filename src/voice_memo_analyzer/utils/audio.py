"""Audio file handling utilities."""

import subprocess
from pathlib import Path
from ..config import MP3_DIR

def convert_m4a_to_mp3(input_path: Path) -> Path:
    """Convert Voice Memo (m4a) to mp3 format using ffmpeg."""
    input_path = Path(input_path)
    output_filename = f"{input_path.stem}_converted.mp3"
    output_path = MP3_DIR / output_filename
    
    # Check if converted file already exists
    if output_path.exists():
        print(f"Using existing converted file: {output_path}")
        return output_path
    
    print(f"Converting {input_path.name} to MP3...")
    try:
        subprocess.run([
            'ffmpeg', '-i', str(input_path), '-acodec', 'libmp3lame',
            '-q:a', '2', str(output_path), '-y'
        ], check=True, capture_output=True, text=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e.stderr}")
        raise

def prepare_audio_file(file_path: Path) -> tuple[Path, Path]:
    """Prepare audio file for processing, converting if necessary.
    
    Returns:
        tuple: (original_path, mp3_path)
    """
    file_path = Path(file_path)
    mp3_file_path = None
    
    if file_path.suffix.lower() == '.m4a':
        mp3_file_path = convert_m4a_to_mp3(file_path)
    elif file_path.suffix.lower() == '.mp3':
        # If it's already an MP3, copy it to the mp3_conversions directory
        output_filename = f"{file_path.stem}_copy.mp3"
        output_path = MP3_DIR / output_filename
        
        # Check if the file is already in mp3_conversions directory
        if file_path != output_path:
            if output_path.exists():
                print(f"Using existing copy: {output_path}")
                mp3_file_path = output_path
            else:
                print(f"Copying {file_path.name} to mp3_conversions directory...")
                output_path.write_bytes(file_path.read_bytes())
                mp3_file_path = output_path
    
    if not mp3_file_path:
        mp3_file_path = file_path  # Use original path if no conversion needed
        
    return file_path, mp3_file_path
