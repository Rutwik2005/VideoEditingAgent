# 2_get_timestamps.py

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

TRANSCRIPT_FILENAME = "transcript.txt"
TIMESTAMPS_FILENAME = "timestamps.json"

def analyze_transcript_with_llm():
    """Sends the transcript to an LLM and gets key timestamps."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    
    genai.configure(api_key=api_key)

    try:
        with open(TRANSCRIPT_FILENAME, "r") as f:
            transcript = f.read()
    except FileNotFoundError:
        print(f"Error: {TRANSCRIPT_FILENAME} not found. Please run the content extraction script first.")
        return

    # This is the prompt engineering part, crucial for good results
    prompt = f"""
    You are an expert video editor. I will provide you with a transcript of a video. 
    Your task is to identify the 5-7 most important, impactful, and concise segments to create a 2-3 minute summary teaser.

    The original video is about 15 minutes long. You must select segments that, when combined, create a coherent and compelling narrative.
    Focus on key insights, conclusions, and moments of high emotional or informational value.

    Provide the output as a JSON array of objects. Each object must contain:
    1. "start_time": The start time of the segment in "MM:SS" format.
    2. "end_time": The end time of the segment in "MM:SS" format.
    3. "justification": A brief, one-sentence explanation of why this segment is important for the teaser.

    Do NOT include any text before or after the JSON array. Your response must be only the JSON.

    Here is the transcript:
    ---
    {transcript}
    ---
    """

    print("Sending transcript to the LLM for analysis...")
    model = genai.GenerativeModel('gemini-2.5-pro') # Using a fast and capable model
    response = model.generate_content(prompt)

    # Clean up the response to ensure it's valid JSON
    cleaned_response = response.text.strip().replace("```json", "").replace("```", "")

    print("LLM analysis complete. Saving timestamps.")
    with open(TIMESTAMPS_FILENAME, "w") as f:
        # We save the cleaned text directly, assuming it's valid JSON
        f.write(cleaned_response)

    print(f"Timestamps saved to {TIMESTAMPS_FILENAME}")
    
if __name__ == "__main__":
    analyze_transcript_with_llm()