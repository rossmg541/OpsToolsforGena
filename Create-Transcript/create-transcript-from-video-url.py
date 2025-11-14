import yt_dlp
from moviepy.editor import VideoFileClip
import sys
import os

# Function to download video from URL
def download_video(url, download_path):
    try:
        ydl_opts = {
            'outtmpl': download_path,  # File path template
            'format': 'best',  # Download best available quality
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Video has been downloaded successfully to {download_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

# Function to extract audio from video
def extract_audio(video_file, audio_file):
    try:
        # Load the video file
        clip = VideoFileClip(video_file)

        # Extract audio from the video clip
        audio = clip.audio

        # Write the audio to an output file (e.g., .mp3 or .wav)
        audio.write_audiofile(audio_file)

        print(f"Audio has been successfully extracted and saved to {audio_file}")

    except Exception as e:
        print(f"Error extracting audio: {e}")

# Example usage
if __name__ == "__main__":
    # Ensure the correct number of arguments
    if len(sys.argv) != 4:
        print("Usage: python script.py <video_url> <download_path> <audio_file>")
    else:
        video_url = sys.argv[1]      # URL of the video
        download_path = sys.argv[2]  # Path to save the downloaded video
        audio_file = sys.argv[3]     # Path to save the audio file (e.g., 'audio.mp3')

        # Download the video
        download_video(video_url, download_path)

        # Extract audio from the downloaded video
        extract_audio(download_path, audio_file)

        # Optionally remove the video file after extracting audio (to clean up)
        if os.path.exists(download_path):
            os.remove(download_path)
            print(f"Deleted the downloaded video: {download_path}")
