import yt_dlp
import os 
import unmix

file = "ytb.txt"
if os.path.exists(file):
    with open(file, "r") as f:
        url = f.read().strip()
else:
    url = "https://youtu.be/Ta2ULGIi2yk?si=gB6H-d5REEg_Md3n"

url = url.replace("&start_radio=1", "")


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "audio.mp3")
output_dir = os.path.join(script_dir, "separated")
unmix.audio_split(input_path, output_dir)
