import click
from faster_whisper import WhisperModel
import os
from app.cli.utils import is_youtube_url, download_youtube_audio, download_file, is_url


@click.command()
@click.argument("input_source")
@click.argument("output_file", default="transcription.txt")
@click.option(
    "--model",
    "-m",
    default="medium",
    help="Model size to use (tiny, base, small, medium, large)",
    show_default=True,
)
@click.option(
    "--device",
    "-d",
    default="auto",
    type=click.Choice(["auto", "cpu", "cuda"]),
    help="Device to use for inference",
    show_default=True,
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Language code for transcription (e.g., en, fr, de). Default: auto-detect",
)
@click.option(
    "--timestamps",
    "-t",
    is_flag=True,
    help="Include timestamps in the transcription output",
)
def transcribe(
    input_source,
    output_file,
    model,
    device,
    language,
    timestamps,
):
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
        whisper_model = WhisperModel(
            model, device=device, compute_type="auto"
        )

        # Perform transcription
        click.echo("Transcribing audio...")
        segments, info = whisper_model.transcribe(input_source, beam_size=5, language=language)

        # Print duration
        click.echo(f"Duration: {info.duration:.2f} seconds")

        # Print detection info
        if language is None:
            click.echo( 
                f"Detected language '{info.language}' with probability {info.language_probability}"
            )

        # Build transcription
        transcription = ""
        grouped_transcription = []
        current_group = ""
        current_start = None

        for segment in segments:
            if timestamps:
                if current_start is None:
                    current_start = segment.start
                current_group += f"{segment.text} "
            else:
                current_group += f"{segment.text} "
            
            # Simple grouping: end the group after each segment
            if timestamps:
                grouped_transcription.append(f"[{current_start:.2f}s -> {segment.end:.2f}s] {current_group.strip()}")
                click.echo(f"[{current_start:.2f}s -> {segment.end:.2f}s] {current_group.strip()}")
                transcription += f"[{current_start:.2f}s -> {segment.end:.2f}s] {current_group.strip()}\n"
                current_group = ""
                current_start = None
            else:
                transcription += segment.text + " "
        
        # Write to output file
        with open(output_file, "w", encoding="utf-8") as f:  # Ensure writing formatted transcription
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
