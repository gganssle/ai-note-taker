"""Analyzes transcribed conversations using OpenAI's GPT models."""

import json
from pathlib import Path
from openai import OpenAI

class ConversationAnalyzer:
    def __init__(self, client: OpenAI):
        self.client = client

    def analyze_transcript(self, formatted_transcript: str) -> dict:
        """Analyze the transcript using GPT-4.
        
        Returns:
            dict: Analysis results containing key moments, summary, and action items
        """
        print("Analyzing conversation...")
        analysis_prompt = f"""
        Analyze this timestamped conversation transcript and provide:
        1. Action items that need to be taken
        2. Overall conversation summary
        3. Key moments with their timestamps
        
        Guidelines:
        - For action items: Make each item detailed and self-contained, so it can be understood without any other context
        - For key moments: Include timestamps [MM:SS] and focus on important decisions or revelations
        - For overall summary: Provide a concise but complete summary of the main points and outcomes
        - Note any important agreements or conclusions reached
        
        Transcript:
        {formatted_transcript}
        
        Format the response as JSON with these keys:
        - action_items (array of strings, each being a complete, self-contained task)
        - overall_summary (string)
        - key_moments (array of objects with 'timestamp' and 'summary' keys)
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3
        )

        return json.loads(response.choices[0].message.content)
