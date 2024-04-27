import os
import yt_dlp as youtube_dl
import assemblyai as aai
import anthropic
from api_keys import api_key_aai, api_key_anthropic

def download_audio_from_youtube(video_url, output_path):

    print("Downloading audio...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True
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

    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        temperature=0,
        messages=[
            {"role": "user", "content": f"Summarize the following text: {text}"}
        ]
    ) as stream:
        print("\n")
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print("\n")

def ask_question(text):
    conversation_history = [
        f"Here is a text: {text}",
        "Based on the given text, I will ask you a series of questions. Please provide concise and relevant answers.",
        "\n\nHuman: Let's begin the conversation.",
        "\n\nAssistant: Understood. Please go ahead and ask your questions based on the provided text. I'll do my best to provide relevant and concise answers.",
    ]

    while True:
        print("\n" + "-" * 50 + "\n")
        question = input("Ask a question (or type 'quit' to exit): ")
        if question.lower() == "quit":
            break

        conversation_history.append(f"\n\nHuman: {question}")
        conversation_history.append("\n\nAssistant:")

        client = anthropic.Anthropic(api_key=api_key_anthropic)
        response = client.completions.create(
            prompt="".join(conversation_history),
            model="claude-v1",
            max_tokens_to_sample=350,
            stop_sequences=["\n\nHuman:"],
            stream=True,
        )

        print("\nAssistant:", end=" ")
        assistant_response = ""
        for data in response:
            token = data.completion
            print(token, end="", flush=True)
            assistant_response += token
        print("\n")

        conversation_history[-1] += f" {assistant_response.strip()}"