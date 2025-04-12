"""Markdown formatting utilities."""

from datetime import datetime
from pathlib import Path

def format_results_as_markdown(results: dict, original_filename: str) -> str:
    """Format analysis results as a markdown document."""
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
