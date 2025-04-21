"""Audio transcription module using OpenAI's Whisper model.

This module handles the transcription of audio files using OpenAI's Whisper model,
providing both raw transcripts and formatted versions with timestamps.
"""

from pathlib import Path
from openai import OpenAI
from ..utils.formatting import format_transcript_with_timestamps

class Transcriber:
    """Handles audio transcription using OpenAI's Whisper model.
    
    This class manages the transcription of audio files, providing both raw
    text output and a formatted version with timestamps. It uses OpenAI's
    Whisper model for high-quality transcription.
    """

    def __init__(self, client: OpenAI):
        """Initialize the transcriber with an OpenAI client.
        
        Args:
            client: An initialized OpenAI client object
        """
        self.client = client

    def transcribe(self, audio_file_path: Path) -> tuple[str, str]:
        """Transcribe an audio file using OpenAI's Whisper model.
        
        Takes an audio file and transcribes it using Whisper, then formats
        the output with timestamps. The audio file should be in a supported
        format (mp3, mp4, mpeg, mpga, m4a, wav, or webm).
        
        Args:
            audio_file_path: Path to the audio file to transcribe
        
        Returns:
            tuple: Contains:
                - raw_transcript (str): Plain text transcript without timestamps
                - formatted_transcript (str): Transcript with [MM:SS] timestamps
        
        Raises:
            FileNotFoundError: If the audio file doesn't exist
            Exception: If there's an error during transcription
        """
        print("Transcribing audio...")
        
        try:
            with open(audio_file_path, 'rb') as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word", "segment"],
                    language="en"
                )
            
            raw_transcript = response.text
            formatted_transcript = format_transcript_with_timestamps(response)
            return raw_transcript, formatted_transcript
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise
