import whisper
import srt
import datetime
import os
import sys

def generate_subtitles(file_path, output_srt="captions.srt", model_size="base"):
    """Generate subtitles using Whisper and save as SRT"""
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        print(f"Loading Whisper model ({model_size})...")
        model = whisper.load_model(model_size)
    except Exception as e:
        print(f"❌ Error loading Whisper model: {e}")
        return

    print("Transcribing...")
    try:
        result = model.transcribe(file_path)
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return

    subtitles = []
    for i, segment in enumerate(result.get("segments", [])):
        start = datetime.timedelta(seconds=segment["start"])
        end = datetime.timedelta(seconds=segment["end"])
        subtitles.append(
            srt.Subtitle(index=i+1, start=start, end=end, content=segment["text"])
        )

    try:
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write(srt.compose(subtitles))
        print(f"✅ Subtitles saved as {output_srt}")
    except Exception as e:
        print(f"❌ Error saving SRT file: {e}")

# ------------------ MAIN ------------------
if __name__ == "__main__":
    file_path = input("Enter audio file path (.mp3 or .wav): ").strip()
    if not file_path:
        print("❌ No file path provided.")
        sys.exit(1)
    generate_subtitles(file_path)