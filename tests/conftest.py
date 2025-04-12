"""Test configuration and fixtures for the voice memo analyzer."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
from openai import OpenAI

@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client for testing."""
    client = Mock(spec=OpenAI)
    
    # Mock audio transcriptions
    mock_audio = MagicMock()
    mock_transcriptions = MagicMock()
    mock_transcription_response = Mock()
    mock_transcription_response.text = "This is a test transcript"
    mock_transcription_response.segments = [
        {
            'start': 0.0,
            'end': 5.0,
            'text': 'This is a test transcript'
        }
    ]
    mock_transcription_response.words = [
        {
            'start': 0.0,
            'end': 1.0,
            'text': 'This'
        },
        {
            'start': 1.0,
            'end': 2.0,
            'text': 'is'
        },
        {
            'start': 2.0,
            'end': 3.0,
            'text': 'a'
        },
        {
            'start': 3.0,
            'end': 4.0,
            'text': 'test'
        },
        {
            'start': 4.0,
            'end': 5.0,
            'text': 'transcript'
        }
    ]
    
    # Mock file handling in transcriptions
    def mock_create(model=None, file=None, response_format=None, timestamp_granularities=None, language=None):
        if isinstance(file, (str, Path)):
            # Handle file path
            if not Path(file).exists():
                raise FileNotFoundError(f"No such file: {file}")
        return mock_transcription_response
    
    mock_transcriptions.create = mock_create
    mock_audio.transcriptions = mock_transcriptions
    client.audio = mock_audio
    
    # Mock chat completions
    mock_chat = MagicMock()
    mock_completions = MagicMock()
    mock_chat_response = Mock()
    mock_chat_response.choices = [
        Mock(
            message=Mock(
                content='''{
                    "action_items": ["Follow up with team about project timeline"],
                    "overall_summary": "Discussion about project planning",
                    "key_moments": [{"timestamp": "00:15", "summary": "Agreed on deadline"}]
                }'''
            )
        )
    ]
    mock_completions.create.return_value = mock_chat_response
    mock_chat.completions = mock_completions
    client.chat = mock_chat
    
    return client

@pytest.fixture
def test_audio_file(tmp_path):
    """Create a temporary test audio file."""
    audio_file = tmp_path / "test_memo.m4a"
    audio_file.write_bytes(b"mock audio content")
    return audio_file

@pytest.fixture
def test_mp3_file(tmp_path):
    """Create a temporary test MP3 file."""
    mp3_file = tmp_path / "test_memo.mp3"
    mp3_file.write_bytes(b"mock mp3 content")
    return mp3_file

@pytest.fixture
def test_data_dirs(tmp_path):
    """Create temporary test data directories."""
    dirs = {
        'cache': tmp_path / 'cache',
        'mp3_conversions': tmp_path / 'mp3_conversions',
        'transcripts': tmp_path / 'transcripts',
        'results': tmp_path / 'results'
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(exist_ok=True)
    
    return dirs
