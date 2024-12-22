# Quill

![Quill Logo](static/logo.jpeg)

A command-line tool for transcribing audio files, YouTube videos, and podcasts using Faster Whisper.

![Demo](static/demo.gif)

## Prerequisites

- ffmpeg
- Python 3.10+

## Installation

```bash
pip install -e .
```

## Usage

```bash
quill INPUT_SOURCE OUTPUT_FILE [--model MODEL] [--device DEVICE] [--language LANGUAGE]

# Examples:
quill audio.mp3 transcript.txt
quill https://youtube.com/watch?v=... transcript.txt
quill https://example.com/audio.mp3 transcript.txt --model large
quill podcast.mp3 output.txt --device cuda --language en
```

Options:

- `--model`: Model size to use (tiny, base, small, medium, large). Default: medium
- `--device`: Device to use for inference (cpu, cuda). Default: cpu
- `--language`: Language code for transcription (e.g., en, fr, de). Default: auto-detect

## Supported Input Sources

- Local audio files (mp3, wav, m4a, etc.)
- YouTube URLs
- Direct URLs to audio files

## Performance Notes

- Using CUDA-enabled GPU significantly improves transcription speed
- Larger models provide better accuracy but require more memory and processing time
- The 'medium' model provides a good balance between speed and accuracy for most use cases

## License

Apache 2.0
