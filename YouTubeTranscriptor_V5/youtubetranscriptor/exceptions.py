"""
Custom exceptions for the YouTubeTranscriptor module.
"""

class TranscriptError(Exception):
    """Raised when there's an error related to transcript retrieval or processing."""
    pass

class VideoError(Exception):
    """Raised when there's an error related to video URL or ID."""
    pass
