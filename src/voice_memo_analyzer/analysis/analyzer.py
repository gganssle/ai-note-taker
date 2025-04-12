"""Conversation analysis module using OpenAI's GPT models.

This module handles the analysis of transcribed conversations using OpenAI's GPT-4
model to extract key information like action items, summaries, and important moments.
"""

import json
from pathlib import Path
from openai import OpenAI

class ConversationAnalyzer:
    """Analyzes transcribed conversations using OpenAI's GPT models.
    
    This class is responsible for processing transcribed text to extract:
    - Action items that need to be taken
    - Overall conversation summary
    - Key moments with their timestamps
    
    It uses GPT-4 to analyze the text and structure the results in a consistent format.
    """

    def __init__(self, client: OpenAI):
        """Initialize the analyzer with an OpenAI client.
        
        Args:
            client: An initialized OpenAI client object
        """
        self.client = client

    def analyze_transcript(self, formatted_transcript: str) -> dict:
        """Analyze a formatted transcript and extract key information.
        
        Uses GPT-4 to analyze the transcript and extract structured information
        about the conversation, including action items, key moments, and a
        summary.
        
        Args:
            formatted_transcript: The transcript text with timestamps
        
        Returns:
            dict: Analysis results containing:
                - action_items: List of strings, each a complete task
                - overall_summary: String summarizing the conversation
                - key_moments: List of dicts with 'timestamp' and 'summary' keys
        
        Raises:
            Exception: If the OpenAI API call fails
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
        
        try:
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error parsing analysis results: {e}")
            return {
                "action_items": [],
                "overall_summary": "Error analyzing transcript",
                "key_moments": []
            }
