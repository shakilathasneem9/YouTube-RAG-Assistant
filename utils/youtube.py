import yt_dlp

def download_youtube_audio(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio[abr<=128]/bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True,
        'postprocessors': []  # IMPORTANT: no conversion
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename