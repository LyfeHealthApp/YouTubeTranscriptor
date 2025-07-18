"""
YouTubeTranscriptor - A module for extracting transcripts from YouTube videos.
"""

from .transcriptor import YouTubeTranscriptor
from .exceptions import TranscriptError, VideoError

__version__ = "0.1.0"
__all__ = ["YouTubeTranscriptor", "TranscriptError", "VideoError"]
