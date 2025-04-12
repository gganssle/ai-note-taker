# Voice Memo Analyzer

A Python application that processes Mac voice memos using OpenAI's API to provide transcription, analysis, and actionable insights.

## Features

- Converts Voice Memos (m4a) to MP3 format
- Transcribes audio using OpenAI's Whisper model
- Analyzes conversations using GPT-4
- Generates:
  - Action items
  - Overall conversation summary
  - Key moments with timestamps
  - Formatted transcript
- Caches results for efficiency
- Exports results in both JSON and Markdown formats

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-note-taker
   ```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Set up your environment:

Copy .env.example to .env
Add your OpenAI API key:
OPENAI_API_KEY=your-api-key-here

## Usage
Run the analyzer on any voice memo:

```bash
python main.py path/to/voice_memo.m4a
```

The script will:

* Convert the audio to MP3 if needed
* Transcribe the audio
* Analyze the conversation
* Save results in:
  * data/results/ (markdown format)
  * data/transcripts/ (JSON format)

## Project Structure

```
.
├── src/voice_memo_analyzer/    # Main package
│   ├── analysis/              # Conversation analysis
│   ├── transcription/         # Audio transcription
│   └── utils/                 # Utility functions
├── data/                      # Data directory
│   ├── cache/                 # Cached results
│   ├── mp3_conversions/       # Converted audio files
│   ├── results/               # Markdown results
│   └── transcripts/           # JSON results
└── main.py                    # CLI entry point
```

## Requirements
Python 3.8+
ffmpeg (for audio conversion)
OpenAI API key
Dependencies listed in requirements.txt:
openai
python-dotenv
pydub

## Author
Graham Ganssle
grahamganssle@gmail.com

## License
MIT License