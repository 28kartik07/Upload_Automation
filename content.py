import os
import random
import requests
import subprocess
import shutil
import time
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# 1. Random Story Generator with Groq API (Open Source LLM API)
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_story():
    genres = ["Sci-Fi", "Horror", "Love", "Funny", "Crime"]
    prompt = f"Write a {random.choice(genres)} story in 100 words for a short video."
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemma2-9b-it",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Error generating story:", response.text)
        return ""

# 2. Random Game Clip Downloader (yt-dlp) with Auto-Trimming
def download_game_clip():
    game_list = ["minecraft gameplay", "gta funny moments", "roblox obby"]
    query = random.choice(game_list)
    os.makedirs("downloads", exist_ok=True)
    clip_path = os.path.join("downloads", "clip.mp4")
    cmd = f'yt-dlp "ytsearch5:{query}" --max-filesize 50M --max-downloads 1 --dateafter now-1year -f "mp4" -o "{clip_path}"'
    print("Downloading video with command:", cmd)
    os.system(cmd)
    
    if os.path.exists(clip_path):
        print(f"Downloaded clip for: {query}")
        trim_video(clip_path)
    else:
        print("No clip downloaded. Check yt-dlp command or query.")

# 3. Trim Video to 60 Seconds
def trim_video(file_path):
    video = VideoFileClip(file_path).subclipped(0, 60)
    trimmed_path = file_path.replace(".mp4", "_trimmed.mp4")
    video.write_videofile(trimmed_path, codec="libx264")
    print("Trimmed video saved as:", trimmed_path)
    return trimmed_path

# 4. Free AI Voiceover (OpenTTS API - Local TTS Server)
def generate_voiceover(text):
    tts_url = "http://localhost:5002/api/tts"  # Install OpenTTS locally
    response = requests.post(tts_url, json={"text": text, "voice": "en_us"})
    if response.status_code == 200:
        with open("voiceover.wav", "wb") as f:
            f.write(response.content)
        print("Voiceover generated successfully")
    else:
        print("Error generating voiceover:", response.text)

# 5. Auto Video Editing with MoviePy
def auto_edit_video():
    video = VideoFileClip("downloads/clip_trimmed.mp4")
    audio = AudioFileClip("voiceover.wav")
    video = video.with_audio(audio)
    video = video.subclipped(0, min(video.duration, audio.duration))  # Match video duration with voiceover
    video = video.resized(height=1920).resized(width=1080)
    video.write_videofile("final_video.mp4", codec="libx264", fps=30)
    print("🎯 Final Video Rendered Successfully")

# 6. Auto Upload via Instagram + YouTube API (n8n Free Automation)
def auto_upload():
    os.makedirs("uploads", exist_ok=True)  # Create uploads folder if not exists
    shutil.copy("final_video.mp4", "uploads/final_video.mp4")
    print("Video sent to Upload Folder. n8n will automatically upload to social media.")

if __name__ == "__main__":
    print("Starting AI Content Pipeline 🚀")
    story = generate_story()
    print("Generated Story:", story)
    download_game_clip()
    print("Downloaded and Trimmed Game Clip")
    generate_voiceover(story)
    print("Generated Voiceover")
    auto_edit_video()
    print("Edited Video")
    # auto_upload()
    # print("Uploaded Video")

# requirements.txt
# requests
# moviepy
# yt-dlp


