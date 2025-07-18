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

Example input file format:

```csv
Title;Link;Creator
My Video;https://www.youtube.com/watch?v=12345;Channel Name
```

### Running the Script

You can run the script in two ways:

1. Directly with Poetry:

```bash
poetry run python main.py
```

2. Or activate the virtual environment first:

```bash
poetry shell
python main.py
```

### Output

The script will generate `transcripts.csv` containing:

- Title of the video
- Link to the video
- Creator name
- Full transcript text
- Status (Success or Error message)

The output file uses:

- Tab (\t) as the delimiter for better handling of text content
- Proper escaping of special characters
- UTF-8 encoding

This format ensures that commas, quotes, or other special characters in titles or transcripts won't break the CSV structure.

## Features

- Extracts transcripts from YouTube videos
- Supports both auto-generated and manual English transcripts
- Prioritizes auto-generated transcripts if available
- Handles errors gracefully with informative messages
- Robust CSV input/output for batch processing with special character handling
- Safe delimiter handling to preserve transcript and title contents

## Error Handling

The script handles various scenarios:

- Invalid YouTube URLs
- Missing transcripts
- Disabled transcripts
- Various transcript formats
- Special characters in content

## Dependencies

Managed by Poetry:

- pandas: Data processing and CSV handling
- youtube_transcript_api: YouTube transcript extraction

## File Format Details

### Input (videos.csv)

- Delimiter: Semicolon (;)
- Encoding: ISO-8859-1
- Required columns: Title, Link, Creator

### Output (transcripts.csv)

- Delimiter: Tab (\t)
- Encoding: UTF-8
- Special character escaping: Yes
- Columns: Title, Link, Creator, Transcript, Status
