# 1_extract_content.py

import subprocess
import whisper
import os

# The YouTube video URL from the assignment
YOUTUBE_URL = "https://www.youtube.com/watch?v=0FUFewGHLLg"
VIDEO_FILENAME = "source_video.mp4"
AUDIO_FILENAME = "source_audio.mp3"
TRANSCRIPT_FILENAME = "transcript.txt"

def download_video():
    """Downloads the video from YouTube using yt-dlp."""
    print(f"Downloading video from {YOUTUBE_URL}...")
    # Command to download the best quality mp4 video
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--merge-output-format", "mp4",
        "-o", VIDEO_FILENAME,
        YOUTUBE_URL
    ]
    subprocess.run(command, check=True)
    print(f"Video saved as {VIDEO_FILENAME}")

def extract_audio():
    """Extracts audio from the video file using ffmpeg (called by moviepy)."""
    # This is a simple way to call ffmpeg directly for audio extraction
    if not os.path.exists(VIDEO_FILENAME):
        print("Video file not found. Please download it first.")
        return
        
    print("Extracting audio from video...")
    command = [
        "ffmpeg",
        "-i", VIDEO_FILENAME,
        "-q:a", "0",
        "-map", "a",
        AUDIO_FILENAME,
        "-y" # Overwrite output file if it exists
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Audio saved as {AUDIO_FILENAME}")

def transcribe_audio():
    """Transcribes the audio file using OpenAI's Whisper model."""
    if not os.path.exists(AUDIO_FILENAME):
        print("Audio file not found. Please extract it first.")
        return
        
    print("Transcribing audio... (This may take a few minutes)")
    # Load the base model. For higher accuracy, you can use "medium" or "large"
    model = whisper.load_model("base")
    result = model.transcribe(AUDIO_FILENAME)
    
    with open(TRANSCRIPT_FILENAME, "w") as f:
        f.write(result["text"])
        
    print(f"Transcript saved as {TRANSCRIPT_FILENAME}")

if __name__ == "__main__":
    if not os.path.exists(VIDEO_FILENAME):
        download_video()
    if not os.path.exists(AUDIO_FILENAME):
        extract_audio()
    if not os.path.exists(TRANSCRIPT_FILENAME):
        transcribe_audio()
    print("Content extraction complete.")