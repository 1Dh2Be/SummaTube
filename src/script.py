import os
import yt_dlp as youtube_dl
import assemblyai as aai
import anthropic

def download_audio_from_youtube(video_url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
        'outtmpl': os.path.join(output_path, 'audio'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print(f"Audio downloaded from {video_url} and saved as audio.mp3")
    return os.path.join(output_path, "audio.mp3")

def speech_to_text(file):
    aai.settings.api_key = "3b001a9f39e04c1e8b1accd33d9f84ef"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    text = transcript.text
    return text

def summarize_text(text):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": f"Summarize the following text: {text}"
}
        ]
    )
    print(message.content[0].text)