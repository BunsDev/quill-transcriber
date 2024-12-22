import click
from faster_whisper import WhisperModel
import os
from app.cli.utils import is_youtube_url, download_youtube_audio, download_file, is_url


@click.command()
@click.argument("input_source")
@click.argument("output_file", default="transcription.txt")
@click.option(
    "--model",
    default="medium",
    help="Model size to use (tiny, base, small, medium, large)",
    show_default=True,
)
def transcribe(input_source, output_file="transcription.txt", model="medium"):
    """
    Transcribe audio from a file or URL to text.

    INPUT_SOURCE: Path to local audio file or URL to audio file (including YouTube URLs)

    OUTPUT_FILE: Path where the transcription will be saved
    """
    temp_file = None
    try:
        # Handle URL input
        if is_url(input_source):
            if is_youtube_url(input_source):
                click.echo("Detected YouTube URL. Downloading audio...")
                temp_file = "temp_audio_file"
                input_source = download_youtube_audio(input_source, temp_file)
            else:
                temp_file = "temp_audio_file"
                input_source = download_file(input_source, temp_file)

        # Initialize the model
        click.echo("Loading model...")
        whisper_model = WhisperModel(model, device="auto", compute_type="auto")

        # Perform transcription
        click.echo("Transcribing audio...")
        segments, info = whisper_model.transcribe(input_source, beam_size=5)

        # Print detection info
        click.echo(
            f"Detected language '{info.language}' with probability {info.language_probability}"
        )

        # Build transcription
        transcription = ""
        for segment in segments:
            click.echo(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
            transcription += segment.text

        # Write to output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcription)

        click.echo(f"\nTranscription saved to: {output_file}")

    except KeyboardInterrupt:
        click.echo("\nTranscription cancelled by user. Cleaning up...")
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        raise click.Abort()

    except Exception as e:
        raise click.ClickException(str(e))

    finally:
        # Cleanup downloaded files
        if temp_file:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(f"{temp_file}.wav"):
                os.remove(f"{temp_file}.wav")
