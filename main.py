#!/usr/bin/env python3
"""Command-line interface for the voice memo analyzer.

This script provides a command-line interface for processing voice memos using
the VoiceMemoAnalyzer. It handles basic argument validation and error reporting.

Usage:
    1. Command line: python main.py <path_to_audio_file>
    2. Drag and drop: Run python main.py and drag the audio file into the terminal

The script will process the audio file and display the results, including:
- Action items extracted from the conversation
- Overall conversation summary
- Key moments with timestamps
- Full transcript with timestamps
"""

import sys
from pathlib import Path
from src.voice_memo_analyzer import VoiceMemoAnalyzer

def get_audio_file() -> Path:
    """Get the audio file path from either command line args or user input.
    
    Returns:
        Path: Path object for the audio file
        
    Raises:
        SystemExit: If no valid file is provided
    """
    if len(sys.argv) == 2:
        # File provided as command line argument
        return Path(sys.argv[1])
    
    # No command line argument, prompt for drag and drop
    print("Please drag and drop your audio file into the terminal, then press Enter:")
    file_path = input().strip()
    
    # Clean up the file path (remove quotes and escape characters)
    file_path = file_path.strip("'\"").replace("\\", "")
    return Path(file_path)

def main():
    """Process a voice memo file and display analysis results.
    
    Command-line interface that validates the input file, processes it through
    the VoiceMemoAnalyzer, and displays the results. The audio file can be
    either m4a (Voice Memo) or mp3 format.
    
    Args:
        None (uses sys.argv or user input)
    
    Returns:
        None
    
    Raises:
        SystemExit: If no valid file is provided or if the file doesn't exist
    """
    try:
        audio_file = get_audio_file()
        if not audio_file.exists():
            print(f"Error: File not found: {audio_file}")
            sys.exit(1)

        analyzer = VoiceMemoAnalyzer()
        results = analyzer.analyze_audio(audio_file)
        analyzer.display_results(results)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
