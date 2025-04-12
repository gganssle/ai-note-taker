#!/usr/bin/env python3
"""Command-line interface for the voice memo analyzer."""

import sys
from pathlib import Path
from src.voice_memo_analyzer import VoiceMemoAnalyzer

def main():
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
