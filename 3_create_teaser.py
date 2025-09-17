# 3_create_teaser.py

import json
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

VIDEO_FILENAME = "source_video.mp4"
TIMESTAMPS_FILENAME = "timestamps.json"
OUTPUT_FILENAME = "teaser_video.mp4"

def time_str_to_seconds(time_str):
    """Converts a 'MM:SS' string to seconds."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

def create_video():
    """Creates the final teaser video based on the timestamps."""
    if not os.path.exists(VIDEO_FILENAME) or not os.path.exists(TIMESTAMPS_FILENAME):
        print("Error: Source video or timestamps file not found. Please run previous scripts.")
        return

    with open(TIMESTAMPS_FILENAME, "r") as f:
        try:
            timestamps = json.load(f)
        except json.JSONDecodeError:
            print("Error: Could not decode JSON from timestamps file. Check the file for errors.")
            return

    print("Loading source video...")
    full_video = VideoFileClip(VIDEO_FILENAME)
    
    clips = []
    print("Cutting video into snippets based on timestamps...")
    for segment in timestamps:
        start_time = time_str_to_seconds(segment['start_time'])
        end_time = time_str_to_seconds(segment['end_time'])
        print(f"  - Creating clip from {segment['start_time']} to {segment['end_time']}")
        
        # Create a subclip from the main video
        clip = full_video.subclip(start_time, end_time)
        clips.append(clip)

    if not clips:
        print("No clips were created. Exiting.")
        return

    print("Merging snippets into the final teaser video...")
    final_clip = concatenate_videoclips(clips)
    
    # Write the final video file
    final_clip.write_videofile(OUTPUT_FILENAME, codec="libx264", audio_codec="aac")

    # Close the clips to free up resources
    full_video.close()
    for clip in clips:
        clip.close()

    print(f"Teaser video successfully created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    create_video()