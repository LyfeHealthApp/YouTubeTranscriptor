#!/usr/bin/env python3
"""
Command-line script for extracting YouTube video transcripts.
"""

import argparse
import sys
from youtubetranscriptor import YouTubeTranscriptor, TranscriptError, VideoError

def main():
    parser = argparse.ArgumentParser(description='Extract transcripts from YouTube videos.')
    parser.add_argument('--input', '-i', default='videos.csv',
                      help='Input CSV file path (default: videos.csv)')
    parser.add_argument('--output', '-o', default='transcripts.csv',
                      help='Output CSV file path (default: transcripts.csv)')
    parser.add_argument('--language', '-l', default='en',
                      help='Language code for transcripts (default: en)')
    args = parser.parse_args()

    try:
        transcriptor = YouTubeTranscriptor(language=args.language)
        df = transcriptor.process_videos(args.input, args.output)
        
        # Print summary
        total = len(df)
        successful = len(df[df['Status'] == 'Success'])
        print(f"\nProcessing complete!")
        print(f"Total videos processed: {total}")
        print(f"Successfully transcribed: {successful}")
        print(f"Failed: {total - successful}")
        print(f"\nResults saved to: {args.output}")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
