import os
import yt_dlp as youtube_dl
import assemblyai as aai
import anthropic
from api_keys import api_key_aai, api_key_anthropic

def download_audio_from_youtube(video_url, output_path):
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        title = info['id']
        print(f"Audio downloaded from {video_url} and saved as {title}")
    return title

def speech_to_text(file):
    aai.settings.api_key = api_key_aai
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    text = transcript.text
    return text

def summarize_text(text):
    client = anthropic.Anthropic(api_key=api_key_anthropic)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0,
        messages=[
            {"role": "user", "content": f"Summarize the following text: {text}"
}
        ]
    )
    sum_text = message.content[0].text
    return sum_text

def save_output_to_txt(output, title ):
    try:
        # Get the local path in the src folder
        path = "src/summaries"

        # Create the file path on the desktop with the specified file name
        file_path = os.path.join(path, title + ".txt")
        
        with open(file_path, 'w') as file:
            file.write(output)
        print("Output saved to", "src/summaries")
    except IOError:
        print("Error: Unable to write to file", "src/summaries")
