# Quill

A command-line tool for transcribing audio using Faster Whisper.

## Prerequisites

- ffmpeg
- Python 3.7+

## Installation

```bash
pip install -e .
```

## Usage

```bash
quill INPUT_SOURCE OUTPUT_FILE [--model MODEL]

# Examples:
quill audio.mp3 transcript.txt
quill https://youtube.com/watch?v=... transcript.txt
quill https://example.com/audio.mp3 transcript.txt --model large
```

Options:
- `--model`: Model size to use (tiny, base, small, medium, large). Default: medium

## Supported Input Sources

- Local audio files
- YouTube URLs
- Direct URLs to audio files
