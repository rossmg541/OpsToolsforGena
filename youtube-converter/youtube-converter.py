import yt_dlp

def download_youtube_video(url, save_path="."):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',  # Will merge to MP4 if codecs allow
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    download_youtube_video(youtube_url, "./")

