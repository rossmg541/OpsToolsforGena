# YouTube Audio Extractor

A simple Python script that downloads videos from YouTube (and other video platforms) and extracts the audio into an MP3 file.

## What Does This Do?

This script takes any YouTube video URL, downloads the video, extracts just the audio portion, and saves it as an audio file (like MP3). The original video file is automatically deleted after extraction to save space. Perfect for:

- Converting YouTube videos to MP3s for offline listening
- Extracting audio from podcasts or lectures
- Creating audio files from music videos
- Saving audio from educational content

## Before You Start

You'll need Python installed on your computer and a few additional tools.

### Check if Python is Installed

1. Open your terminal (Mac) or command prompt (Windows)
2. Type: `python --version` or `python3 --version`
3. If you see a version number (like "Python 3.9.0"), you're good to go!

### Install Python (if needed)

- **Windows**: Download from [python.org](https://www.python.org/downloads/) and run the installer
- **Mac**: Python 3 usually comes pre-installed. If not, download from [python.org](https://www.python.org/downloads/)
- **Linux**: Usually pre-installed. If not, use: `sudo apt-get install python3`

## Installation

### Step 1: Download the Script

1. Download the `audio_extractor.py` file to your computer
2. Save it in a folder you'll remember (like your Documents or Downloads folder)

### Step 2: Install Required Libraries

This script needs several Python libraries and one system dependency. Follow these steps carefully:

#### Install Python Libraries

Open your terminal or command prompt and run:

```bash
pip install yt-dlp moviepy
```

Or if that doesn't work:

```bash
pip3 install yt-dlp moviepy
```

#### Install FFmpeg (Required!)

FFmpeg is a tool that handles video and audio processing. You must install it for this script to work.

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the downloaded file
3. Add the `bin` folder to your system PATH
4. Or use Chocolatey: `choco install ffmpeg`

**Mac:**
```bash
brew install ffmpeg
```
(If you don't have Homebrew, install it from [brew.sh](https://brew.sh))

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Verify FFmpeg Installation:**
```bash
ffmpeg -version
```
You should see version information if it's installed correctly.

## How to Use

### Basic Command Structure

```bash
python audio_extractor.py <video_url> <video_filename> <audio_filename>
```

### Step-by-Step Example

Let's extract audio from a YouTube video:

1. **Copy the video URL** from YouTube (e.g., `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)

2. **Open your terminal** and navigate to where you saved the script

3. **Run the command**:
   ```bash
   python audio_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "temp_video.mp4" "my_audio.mp3"
   ```

### Understanding the Command Parts

- `python audio_extractor.py` - Runs the script
- `"https://www.youtube.com/watch?v=dQw4w9WgXcQ"` - The video URL (use quotes!)
- `"temp_video.mp4"` - Temporary name for the downloaded video (will be deleted automatically)
- `"my_audio.mp3"` - Name for your final audio file

### More Examples

**Extract audio from a podcast:**
```bash
python audio_extractor.py "https://youtube.com/watch?v=abc123" "podcast.mp4" "podcast_episode_1.mp3"
```

**Save as WAV instead of MP3:**
```bash
python audio_extractor.py "https://youtube.com/watch?v=xyz789" "temp.mp4" "audio.wav"
```

**Use full file paths:**
```bash
python audio_extractor.py "https://youtube.com/watch?v=abc123" "/Users/yourname/Desktop/temp.mp4" "/Users/yourname/Music/song.mp3"
```

## What Happens When You Run It

1. **Downloads the video** - The script fetches the best quality version available
2. **Extracts the audio** - Pulls out just the audio track
3. **Saves the audio file** - Creates your MP3 (or WAV) file
4. **Cleans up** - Automatically deletes the temporary video file to save space

## File Formats

You can save audio in different formats by changing the file extension:

- `.mp3` - Most common, works everywhere (recommended)
- `.wav` - Higher quality, larger file size
- `.m4a` - Good quality, smaller than WAV
- `.flac` - Lossless quality, large file size

## Troubleshooting

### "Command not found" or "python is not recognized"

- Try using `python3` instead of `python`
- Ensure Python is installed and in your system PATH

### "No module named 'yt_dlp'" or "'moviepy'"

- Run the installation command again: `pip install yt-dlp moviepy`
- Try `pip3` instead of `pip`

### "Error downloading video"

- **Check the URL** - Make sure it's correct and the video is publicly available
- **Age-restricted videos** - These may not work
- **Private videos** - Cannot be downloaded
- **Geographic restrictions** - Some videos aren't available in all countries
- **Update yt-dlp**: `pip install --upgrade yt-dlp`

### "FFmpeg not found" or audio extraction fails

- **Install FFmpeg** - This is the most common issue. See installation instructions above
- **Check FFmpeg installation**: Run `ffmpeg -version` in terminal
- **Add to PATH** - Make sure FFmpeg is in your system PATH

### "Permission denied" errors

- Make sure you have write permissions in the folder
- Try saving files to your Documents or Desktop folder
- On Mac/Linux, don't use system directories without `sudo`

### Downloads are slow

- This is normal for large videos
- Speed depends on your internet connection
- The script shows progress as it downloads

### Script says "Usage: python script.py..."

- You're missing one or more required arguments
- Make sure you include all three: URL, video filename, and audio filename
- Use quotes around the URL

## Important Notes

### Legal and Ethical Usage

- **Only download content you have permission to download**
- Respect copyright laws in your country
- Don't distribute copyrighted content
- This tool is for personal use and backups of content you own or have rights to

### Supported Platforms

While called "YouTube Audio Extractor," this script actually works with many video platforms:
- YouTube
- Vimeo
- Dailymotion
- Twitter videos
- Facebook videos
- And many more (1000+ sites supported by yt-dlp)

### Storage Space

- Videos can be large (100MB - 1GB+)
- The script deletes the video file automatically, keeping only the audio
- Make sure you have enough disk space for the temporary video download

## Tips for Best Results

1. **Use quotes** around the video URL to avoid issues with special characters
2. **Simple filenames** work best - avoid spaces and special characters
3. **Test with a short video first** to make sure everything works
4. **Check disk space** before downloading very long videos
5. **Use .mp3 format** for best compatibility across devices
6. **Update yt-dlp regularly** to fix issues with YouTube changes: `pip install --upgrade yt-dlp`

## Advanced Usage

### Keep the video file (don't auto-delete)

Edit the script and comment out or remove these lines at the end:
```python
if os.path.exists(download_path):
    os.remove(download_path)
    print(f"Deleted the downloaded video: {download_path}")
```

### Download specific quality

The script downloads "best" quality by default. You can modify the `ydl_opts` in the script to change this.

## Quick Reference

**Basic command:**
```bash
python audio_extractor.py "VIDEO_URL" "temp_video.mp4" "output_audio.mp3"
```

**Check if FFmpeg is installed:**
```bash
ffmpeg -version
```

**Update yt-dlp:**
```bash
pip install --upgrade yt-dlp
```

## Need Help?

If you encounter issues:

1. ✅ Check that FFmpeg is installed: `ffmpeg -version`
2. ✅ Verify all libraries are installed: `pip list | grep yt-dlp`
3. ✅ Make sure the video URL is publicly accessible
4. ✅ Try a different, shorter video to test
5. ✅ Check you have enough disk space
6. ✅ Update yt-dlp: `pip install --upgrade yt-dlp`

---

**Disclaimer**: This tool is for personal use only. Always respect copyright laws and the terms of service of video platforms. Only download content you have the right to download.

**License**: Free to use and modify for personal, non-commercial purposes.
