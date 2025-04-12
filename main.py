#!/usr/bin/env python3
"""Command-line interface for the voice memo analyzer.

This script provides a command-line interface for processing voice memos using
the VoiceMemoAnalyzer. It handles basic argument validation and error reporting.

Usage:
    python main.py <path_to_audio_file>

The script will process the audio file and display the results, including:
- Action items extracted from the conversation
- Overall conversation summary
- Key moments with timestamps
- Full transcript with timestamps
"""

import sys
from pathlib import Path
from src.voice_memo_analyzer import VoiceMemoAnalyzer

def main():
    """Process a voice memo file and display analysis results.
    
    Command-line interface that validates the input file, processes it through
    the VoiceMemoAnalyzer, and displays the results. The audio file can be
    either m4a (Voice Memo) or mp3 format.
    
    Args:
        None (uses sys.argv)
    
    Returns:
        None
    
    Raises:
        SystemExit: If no file is provided or if the file doesn't exist
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_audio_file>")
        sys.exit(1)

    audio_file = Path(sys.argv[1])
    if not audio_file.exists():
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)

    analyzer = VoiceMemoAnalyzer()
    results = analyzer.analyze_audio(audio_file)
    analyzer.display_results(results)

if __name__ == "__main__":
    main()
