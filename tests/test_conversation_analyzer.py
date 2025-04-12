"""Tests for the ConversationAnalyzer class."""

import pytest
from src.voice_memo_analyzer.analysis.analyzer import ConversationAnalyzer

def test_conversation_analyzer_initialization(mock_openai_client):
    """Test that the conversation analyzer initializes correctly."""
    analyzer = ConversationAnalyzer(mock_openai_client)
    assert analyzer.client == mock_openai_client

def test_analyze_transcript_success(mock_openai_client):
    """Test successful transcript analysis."""
    analyzer = ConversationAnalyzer(mock_openai_client)
    test_transcript = "[00:00] This is a test transcript."
    
    results = analyzer.analyze_transcript(test_transcript)
    
    assert isinstance(results, dict)
    assert 'action_items' in results
    assert 'overall_summary' in results
    assert 'key_moments' in results
    assert isinstance(results['action_items'], list)
    assert isinstance(results['overall_summary'], str)
    assert isinstance(results['key_moments'], list)
    assert len(results['key_moments']) > 0
    assert 'timestamp' in results['key_moments'][0]
    assert 'summary' in results['key_moments'][0]

def test_analyze_transcript_api_error(mock_openai_client):
    """Test handling of API errors during analysis."""
    analyzer = ConversationAnalyzer(mock_openai_client)
    mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception) as exc_info:
        analyzer.analyze_transcript("Test transcript")
    assert "API Error" in str(exc_info.value)

def test_analyze_transcript_invalid_response(mock_openai_client):
    """Test handling of invalid JSON response from API."""
    analyzer = ConversationAnalyzer(mock_openai_client)
    mock_openai_client.chat.completions.create.return_value.choices[0].message.content = "Invalid JSON"
    
    results = analyzer.analyze_transcript("Test transcript")
    
    assert results['action_items'] == []
    assert results['overall_summary'] == "Error analyzing transcript"
    assert results['key_moments'] == []
