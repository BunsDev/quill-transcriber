import re
import urllib.request
import yt_dlp
import click


def is_youtube_url(url):
    """Check if the URL is a YouTube URL."""
    youtube_patterns = [
        r"^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+",
        r"^https?://(?:www\.)?youtube\.com/v/[\w-]+",
        r"^https?://youtu\.be/[\w-]+",
        r"^https?://(?:www\.)?youtube\.com/shorts/[\w-]+",
    ]
    return any(re.match(pattern, url) for pattern in youtube_patterns)


def download_youtube_audio(url, output_path):
    """Download audio from YouTube video."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info first
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "video")
            # Then download
            ydl.download([url])
        return f"{output_path}.wav", title
    except Exception as e:
        raise click.ClickException(f"Failed to download YouTube audio: {str(e)}")


def download_file(url, local_filename):
    """Download a file from a URL to a local file."""
    try:
        with urllib.request.urlopen(url) as response:
            with open(local_filename, "wb") as f:
                f.write(response.read())
        return local_filename
    except Exception as e:
        raise click.ClickException(f"Failed to download file: {str(e)}")


def is_url(string):
    """Check if a string is a URL."""
    return string.startswith(("http://", "https://"))
