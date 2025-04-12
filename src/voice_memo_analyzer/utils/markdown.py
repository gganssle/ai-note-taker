"""Markdown formatting utilities for analysis results.

This module provides functions to format analysis results into well-structured
markdown documents for easy reading and sharing.
"""

from datetime import datetime
from pathlib import Path

def format_results_as_markdown(results: dict, original_filename: str) -> str:
    """Format analysis results as a markdown document.
    
    Takes the analysis results dictionary and formats it into a structured
    markdown document with sections for action items, summary, key moments,
    and the full transcript.
    
    Args:
        results: Dictionary containing analysis results with keys:
            - action_items: List of action items
            - overall_summary: Conversation summary
            - key_moments: List of dicts with timestamp and summary
            - formatted_transcript: Full transcript with timestamps
        original_filename: Name of the original audio file
    
    Returns:
        str: Formatted markdown content with sections for:
            - Action Items (bullet points)
            - Overall Summary (paragraph)
            - Key Moments (timestamped list)
            - Full Transcript (code block)
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md_lines = [
        f"# Voice Memo Analysis: {Path(original_filename).stem}",
        f"*Analyzed on: {now}*\n",
        
        "## Action Items",
    ]
    
    for item in results['action_items']:
        md_lines.append(f"- {item}")
    
    md_lines.extend([
        "\n## Overall Summary",
        results['overall_summary'],
        
        "\n## Key Moments"
    ])
    
    for moment in results['key_moments']:
        md_lines.append(f"- [{moment['timestamp']}] {moment['summary']}")
    
    md_lines.extend([
        "\n## Full Transcript",
        "```",
        results['formatted_transcript'],
        "```"
    ])
    
    return "\n".join(md_lines)
