"""
Core functionality for extracting transcripts from YouTube videos.
"""

import re
from typing import Optional, Dict, List, Union
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

from .exceptions import TranscriptError, VideoError

class YouTubeTranscriptor:
    """A class to handle YouTube transcript extraction and processing."""
    
    def __init__(self, language: str = 'en'):
        """
        Initialize the YouTubeTranscriptor.

        Args:
            language (str, optional): Language code for transcripts. Defaults to 'en'.
        """
        self.language = language

    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extract video ID from a YouTube URL.

        Args:
            url (str): YouTube video URL.

        Returns:
            str: Video ID.

        Raises:
            VideoError: If video ID cannot be extracted.
        """
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard and shared URLs
            r'youtu\.be\/([0-9A-Za-z_-]{11})',   # Short URLs
        ]

        for pattern in patterns:
            if match := re.search(pattern, url):
                return match.group(1)
        
        raise VideoError(f"Could not extract video ID from URL: {url}")

    def get_transcript(self, video_id: str) -> str:
        """
        Get transcript for a video.

        Args:
            video_id (str): YouTube video ID.

        Returns:
            str: Full transcript text.

        Raises:
            TranscriptError: If transcript cannot be retrieved or processed.
        """
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get auto-generated transcript first
            transcript = None
            try:
                transcript = transcript_list.find_generated_transcript([self.language])
            except NoTranscriptFound:
                # Try manual transcript if auto-generated not found
                try:
                    transcript = transcript_list.find_manually_created_transcript([self.language])
                except NoTranscriptFound:
                    pass

            if transcript is None:
                raise TranscriptError(f"No {self.language} transcript found for video {video_id}")
            
            transcript_data = transcript.fetch()
            
            # Handle different transcript formats
            if isinstance(transcript_data, list):
                return " ".join(str(item.get('text', '')) for item in transcript_data)
            elif hasattr(transcript_data, 'text'):
                return str(transcript_data.text)
            else:
                return " ".join(str(item) for item in transcript_data)

        except (TranscriptsDisabled, NoTranscriptFound) as e:
            raise TranscriptError(f"Could not retrieve transcript: {str(e)}")
        except Exception as e:
            raise TranscriptError(f"Unexpected error: {str(e)}")

    def process_videos(self, input_file: str, output_file: str) -> pd.DataFrame:
        """
        Process multiple videos from a CSV file.

        Args:
            input_file (str): Path to input CSV file.
            output_file (str): Path to output CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the results.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If required columns are missing.
        """
        try:
            df = pd.read_csv(input_file, sep=';', encoding='ISO-8859-1')
            required_columns = {'Title', 'Link', 'Creator'}
            if not required_columns.issubset(df.columns):
                raise ValueError(f"Missing required columns. Required: {required_columns}")

            results = []
            for _, row in df.iterrows():
                try:
                    video_id = self.extract_video_id(row['Link'])
                    transcript = self.get_transcript(video_id)
                    results.append({
                        'Title': row['Title'],
                        'Link': row['Link'],
                        'Creator': row['Creator'],
                        'Transcript': transcript,
                        'Status': 'Success'
                    })
                except (VideoError, TranscriptError) as e:
                    results.append({
                        'Title': row['Title'],
                        'Link': row['Link'],
                        'Creator': row['Creator'],
                        'Transcript': '',
                        'Status': f'Error: {str(e)}'
                    })

            result_df = pd.DataFrame(results)
            # Use tab as delimiter and escape special characters to handle any special characters in content
            result_df.to_csv(output_file, index=False, sep='\t', escapechar='\\', doublequote=False)
            return result_df

        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {input_file}")
        except pd.errors.EmptyDataError:
            raise ValueError("Input file is empty")
        except Exception as e:
            raise Exception(f"Error processing videos: {str(e)}")
