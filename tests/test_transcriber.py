"""Tests for the Transcriber class."""

import pytest
from pathlib import Path
from src.voice_memo_analyzer.transcription.transcriber import Transcriber

def test_transcriber_initialization(mock_openai_client):
    """Test that the transcriber initializes correctly."""
    transcriber = Transcriber(mock_openai_client)
    assert transcriber.client == mock_openai_client

def test_transcribe_success(mock_openai_client, test_mp3_file):
    """Test successful transcription of an audio file."""
    transcriber = Transcriber(mock_openai_client)
    raw_transcript, formatted_transcript = transcriber.transcribe(test_mp3_file)
    
    assert raw_transcript == "This is a test transcript"
    assert formatted_transcript.startswith("[00:00]")
    assert "This is a test transcript" in formatted_transcript

def test_transcribe_file_not_found(mock_openai_client):
    """Test handling of non-existent audio file."""
    transcriber = Transcriber(mock_openai_client)
    
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe(Path('nonexistent.mp3'))

def test_transcribe_api_error(mock_openai_client, test_mp3_file):
    """Test handling of API errors during transcription."""
    transcriber = Transcriber(mock_openai_client)
    
    # Mock API error
    def mock_create(*args, **kwargs):
        raise Exception("API Error")
    mock_openai_client.audio.transcriptions.create = mock_create
    
    with pytest.raises(Exception) as exc_info:
        transcriber.transcribe(test_mp3_file)
    assert "API Error" in str(exc_info.value)
