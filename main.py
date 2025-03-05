import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from instagrapi import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Download YouTube Video
def download_video(url, output_path="video.mp4"):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Downloaded: {output_path}")

# Split Video into 1-Minute Chunks
def split_video(video_path, chunk_length=60, output_folder="chunks"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    video = VideoFileClip(video_path)
    duration = video.duration
    
    for i in range(0, int(duration), chunk_length):
        chunk = video.subclip(i, min(i + chunk_length, duration))
        part_number = i // chunk_length + 1
        chunk_filename = f"{output_folder}/chunk_{part_number}.mp4"
        chunk.write_videofile(chunk_filename, codec="libx264")
        print(f"Saved: {chunk_filename}")

# Upload to Instagram
def upload_video(username, password, folder="chunks"):
    cl = Client()
    cl.login(username, password)
    
    for file in sorted(os.listdir(folder)):
        if file.endswith(".mp4"):
            video_path = os.path.join(folder, file)
            cl.clip_upload(video_path, caption="Automated Upload")
            print(f"Uploaded: {video_path}")

if __name__ == "__main__":
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    YOUTUBE_URL = "https://www.youtube.com/watch?v=ZjVhnMr3vAo"
    download_video(YOUTUBE_URL)
    split_video("video.mp4")
    upload_video(username, password)

