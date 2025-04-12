"""Handles audio transcription using OpenAI's Whisper model."""

from pathlib import Path
from openai import OpenAI
from ..utils.formatting import format_transcript_with_timestamps

class Transcriber:
    def __init__(self, client: OpenAI):
        self.client = client

    def transcribe(self, audio_file_path: Path) -> tuple[str, str]:
        """Transcribe audio file using OpenAI's Whisper model.
        
        Returns:
            tuple: (raw_transcript, formatted_transcript)
        """
        print("Transcribing audio...")
        with open(audio_file_path, 'rb') as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language="en"
            )
        
        formatted_transcript = format_transcript_with_timestamps(response)
        return response.text, formatted_transcript
