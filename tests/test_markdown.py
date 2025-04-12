"""Tests for the markdown formatting utilities."""

from datetime import datetime
from src.voice_memo_analyzer.utils.markdown import format_results_as_markdown

def test_format_results_as_markdown():
    """Test markdown formatting of analysis results."""
    test_results = {
        'action_items': ['Task 1', 'Task 2'],
        'overall_summary': 'Test summary',
        'key_moments': [
            {'timestamp': '00:15', 'summary': 'Test moment 1'},
            {'timestamp': '00:30', 'summary': 'Test moment 2'}
        ],
        'formatted_transcript': '[00:00] Test transcript'
    }
    
    markdown = format_results_as_markdown(test_results, "test_memo.m4a")
    
    # Check all sections are present
    assert "# Voice Memo Analysis: test_memo" in markdown
    assert "*Analyzed on: " in markdown
    assert "## Action Items" in markdown
    assert "- Task 1" in markdown
    assert "- Task 2" in markdown
    assert "## Overall Summary" in markdown
    assert "Test summary" in markdown
    assert "## Key Moments" in markdown
    assert "[00:15] Test moment 1" in markdown
    assert "[00:30] Test moment 2" in markdown
    assert "## Full Transcript" in markdown
    assert "```" in markdown
    assert "[00:00] Test transcript" in markdown

def test_format_results_empty_sections():
    """Test markdown formatting with empty sections."""
    test_results = {
        'action_items': [],
        'overall_summary': '',
        'key_moments': [],
        'formatted_transcript': ''
    }
    
    markdown = format_results_as_markdown(test_results, "empty_memo.m4a")
    
    # Check structure is maintained even with empty content
    assert "# Voice Memo Analysis: empty_memo" in markdown
    assert "## Action Items" in markdown
    assert "## Overall Summary" in markdown
    assert "## Key Moments" in markdown
    assert "## Full Transcript" in markdown
    assert "```" in markdown
