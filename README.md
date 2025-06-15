# YouTube Transcriptor

A tool to extract transcripts from YouTube videos.

## Requirements

- Python 3.13
- Poetry (for dependency management)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/YouTubeTranscriptor.git
cd YouTubeTranscriptor
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Usage

### Input File Setup

1. Create a CSV file named `videos.csv` with the following columns:
   - `Title`: Video title
   - `Link`: YouTube video URL
   - `Creator`: Video creator/channel name
   - Use semicolon (;) as the delimiter
   - Use ISO-8859-1 encoding

### Running the Script

You can run the script in two ways:

1. Directly with Poetry:

```bash
poetry run python transcribe_videos.py
```

2. Or activate the virtual environment first:

```bash
poetry shell
python transcribe_videos.py
```

### Output

The script will generate `transcripts.csv` containing:

- Title of the video
- Link to the video
- Creator name
- Full transcript text

## Features

- Extracts transcripts from YouTube videos
- Supports both auto-generated and manual English transcripts
- Prioritizes auto-generated transcripts if available
- Handles errors gracefully with informative messages
- CSV input/output for batch processing

## Error Handling

The script handles various scenarios:

- Invalid YouTube URLs
- Missing transcripts
- Disabled transcripts
- Various transcript formats

## Dependencies

Managed by Poetry:

- pandas: Data processing and CSV handling
- youtube_transcript_api: YouTube transcript extraction
