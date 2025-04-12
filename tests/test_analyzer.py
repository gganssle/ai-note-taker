"""Tests for the main VoiceMemoAnalyzer class."""

import pytest
import subprocess
from pathlib import Path
from src.voice_memo_analyzer import VoiceMemoAnalyzer
from src.voice_memo_analyzer.utils import audio
from src.voice_memo_analyzer import config

def test_analyzer_initialization(mock_openai_client):
    """Test that the analyzer initializes correctly."""
    analyzer = VoiceMemoAnalyzer()
    assert analyzer.client is not None
    assert analyzer.transcriber is not None
    assert analyzer.analyzer is not None

def test_analyze_audio_success(mock_openai_client, test_audio_file, test_data_dirs, monkeypatch):
    """Test successful audio analysis process."""
    # Setup
    analyzer = VoiceMemoAnalyzer()
    analyzer.client = mock_openai_client
    
    # Create test MP3 file and directory
    mp3_dir = test_data_dirs['mp3_conversions']
    mp3_dir.mkdir(parents=True, exist_ok=True)
    test_mp3_path = mp3_dir / 'test_memo_converted.mp3'
    test_mp3_path.write_bytes(b"mock mp3 content")
    
    # Mock config directories
    monkeypatch.setattr(config, 'MP3_DIR', mp3_dir)
    monkeypatch.setattr(config, 'TRANSCRIPT_DIR', test_data_dirs['transcripts'])
    monkeypatch.setattr(config, 'RESULTS_DIR', test_data_dirs['cache'])
    
    # Mock subprocess.run for ffmpeg
    def mock_subprocess_run(*args, **kwargs):
        return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    
    # Mock the audio preparation
    def mock_prepare_audio(file_path):
        return file_path, test_mp3_path
    monkeypatch.setattr(audio, 'prepare_audio_file', mock_prepare_audio)
    
    # Mock transcriber
    def mock_transcribe(file_path):
        return "Test transcript", "[00:00] Test transcript"
    analyzer.transcriber.transcribe = mock_transcribe
    
    # Mock analyzer
    def mock_analyze(transcript):
        return {
            'action_items': ['Test action'],
            'overall_summary': 'Test summary',
            'key_moments': [{'timestamp': '00:00', 'summary': 'Test moment'}]
        }
    analyzer.analyzer.analyze_transcript = mock_analyze
    
    # Create cache directory
    cache_dir = test_data_dirs['cache']
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Create transcripts directory
    transcripts_dir = test_data_dirs['transcripts']
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    
    # Run analysis
    results = analyzer.analyze_audio(test_audio_file)
    
    # Verify results
    assert 'transcript' in results
    assert 'formatted_transcript' in results
    assert 'action_items' in results
    assert 'overall_summary' in results
    assert 'key_moments' in results
    assert len(results['action_items']) > 0
    assert isinstance(results['overall_summary'], str)
    assert len(results['key_moments']) > 0

def test_analyze_audio_file_not_found(mock_openai_client, monkeypatch):
    """Test handling of non-existent audio file."""
    analyzer = VoiceMemoAnalyzer()
    analyzer.client = mock_openai_client
    
    # Mock subprocess.run for ffmpeg
    def mock_subprocess_run(*args, **kwargs):
        raise FileNotFoundError("No such file: nonexistent.m4a")
    monkeypatch.setattr(subprocess, 'run', mock_subprocess_run)
    
    with pytest.raises(FileNotFoundError):
        analyzer.analyze_audio(Path('nonexistent.m4a'))

def test_display_results_success(capsys):
    """Test that results are displayed correctly."""
    analyzer = VoiceMemoAnalyzer()
    test_results = {
        'action_items': ['Task 1', 'Task 2'],
        'overall_summary': 'Test summary',
        'key_moments': [
            {'timestamp': '00:15', 'summary': 'Test moment'}
        ],
        'formatted_transcript': 'Test transcript'
    }
    
    analyzer.display_results(test_results)
    captured = capsys.readouterr()
    
    assert 'Action Items' in captured.out
    assert 'Task 1' in captured.out
    assert 'Overall Summary' in captured.out
    assert 'Test summary' in captured.out
    assert 'Key Moments' in captured.out
    assert '[00:15]' in captured.out
    assert 'Full Transcript' in captured.out
    assert 'Test transcript' in captured.out

def test_display_results_error(capsys):
    """Test error handling in result display."""
    analyzer = VoiceMemoAnalyzer()
    test_results = {'error': 'Test error'}
    
    analyzer.display_results(test_results)
    captured = capsys.readouterr()
    
    assert 'Error:' in captured.out
    assert 'Test error' in captured.out
