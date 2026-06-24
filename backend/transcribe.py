from faster_whisper import WhisperModel

# Load model once when application starts
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using Faster Whisper.

    Args:
        file_path (str): Path to audio file.

    Returns:
        str: Complete transcript text.
    """

    try:
        segments, info = model.transcribe(
            file_path,
            language="en",
            beam_size=1,
            vad_filter=True
        )

        print(f"Detected language: {info.language}")

        transcript_parts = []

        for segment in segments:
            text = segment.text.strip()

            if text:
                transcript_parts.append(text)

        transcript = " ".join(transcript_parts)

        return transcript.strip()

    except Exception as e:
        print(f"Transcription error: {e}")
        return ""