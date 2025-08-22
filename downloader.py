# downloader.py
import yt_dlp
import os
import shutil
from config import TEMP_DIR, PROXY_URL

# Указываем папку с ffmpeg.exe и ffprobe.exe
FFMPEG_PATH = r"C:\ffmpeg\bin"

def download_audio(query: str) -> str:
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # Базовые настройки
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': FFMPEG_PATH,
        'quiet': True,
        'noplaylist': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
    }

    # Добавляем прокси если он настроен
    if PROXY_URL:
        ydl_opts['proxy'] = PROXY_URL
        print(f"Используется прокси: {PROXY_URL.split('@')[-1]}")  # Логируем без логина/пароля

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
        filename = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"
        if not os.path.exists(filename):
            raise FileNotFoundError("Не удалось конвертировать аудио.")
        return filename

def clean_temp():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)