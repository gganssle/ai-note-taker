"""Text formatting utilities."""

def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def format_transcript_with_timestamps(response) -> str:
    """Format the transcript with timestamps from verbose JSON response."""
    formatted_lines = []
    for segment in response.segments:
        start_time = format_timestamp(segment.start)
        text = segment.text.strip()
        formatted_lines.append(f"[{start_time}] {text}")
    return "\n".join(formatted_lines)
