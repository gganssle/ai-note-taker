"""Main analyzer class that orchestrates the voice memo analysis process."""

import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

from .config import TRANSCRIPT_DIR, RESULTS_DIR
from .utils.audio import prepare_audio_file
from .utils.cache import get_file_hash, get_from_cache, save_to_cache
from .utils.markdown import format_results_as_markdown
from .transcription.transcriber import Transcriber
from .analysis.analyzer import ConversationAnalyzer

class VoiceMemoAnalyzer:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.transcriber = Transcriber(self.client)
        self.analyzer = ConversationAnalyzer(self.client)

    def analyze_audio(self, file_path: str | Path) -> dict:
        """Analyze an audio file and return structured results."""
        file_path = Path(file_path)
        original_filename = file_path.name

        # Convert or copy audio file if needed
        original_path, mp3_path = prepare_audio_file(file_path)
        
        try:
            # Check for cached transcript
            transcript_path, cached_data = get_from_cache(original_path)
            
            if cached_data:
                raw_transcript = cached_data['transcript']
                formatted_transcript = cached_data['formatted_transcript']
            else:
                # Transcribe the audio
                raw_transcript, formatted_transcript = self.transcriber.transcribe(mp3_path)

                # Save transcript and update cache
                transcript_filename = f"{Path(original_filename).stem}.txt"
                transcript_path = TRANSCRIPT_DIR / transcript_filename
                transcript_path.write_text(formatted_transcript)
                
                # Update cache
                cache_data = {
                    'transcript_path': str(transcript_path),
                    'mp3_path': str(mp3_path),
                    'transcript': raw_transcript,
                    'formatted_transcript': formatted_transcript,
                    'original_filename': original_filename
                }
                save_to_cache(cache_data, get_file_hash(original_path))
                print(f"Transcript saved to: {transcript_path}")

            # Analyze the transcript
            analysis_results = self.analyzer.analyze_transcript(formatted_transcript)
            
            # Combine all results
            results = {
                'transcript': raw_transcript,
                'formatted_transcript': formatted_transcript,
                **analysis_results
            }
            
            # Save the analysis results
            analysis_filename = f"{Path(original_filename).stem}_analysis.json"
            analysis_path = TRANSCRIPT_DIR / analysis_filename
            analysis_path.write_text(json.dumps(results, indent=2))
            print(f"Analysis saved to: {analysis_path}")
            
            # Save markdown results
            markdown_content = format_results_as_markdown(results, original_filename)
            markdown_filename = f"{Path(original_filename).stem}_analysis.md"
            markdown_path = RESULTS_DIR / markdown_filename
            markdown_path.write_text(markdown_content)
            print(f"Markdown results saved to: {markdown_path}")
            
            return results
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return {"error": str(e)}

    def display_results(self, results: dict) -> None:
        """Display analysis results in a formatted way."""
        if "error" in results:
            print(f"\nError: {results['error']}")
            return

        print("\n=== Full Transcript ===")
        print(results['formatted_transcript'])

        print("\n=== Key Moments ===")
        for moment in results['key_moments']:
            print(f"[{moment['timestamp']}] {moment['summary']}")
        
        print("\n=== Overall Summary ===")
        print(results['overall_summary'])
        
        print("\n=== Action Items ===")
        for item in results['action_items']:
            print(f"• {item}")
