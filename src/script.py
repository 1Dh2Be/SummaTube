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

def get_completion(api_endpoint=None, conversation_history=None, model="claude-3-sonnet-20240229", max_tokens=1024, stop_sequences=["\n\nHuman:"], stream=False):
    client = anthropic.Anthropic(api_key=api_key_anthropic)

    if api_endpoint == "completions":
        response = client.completions.create(
            prompt="".join(conversation_history),
            model=model,
            max_tokens_to_sample=max_tokens,
            stop_sequences=stop_sequences,
            stream=stream,
        )
    elif api_endpoint == "messages":
        response = client.messages.stream(
            messages=conversation_history,
            model=model,
            max_tokens=max_tokens,
            stop_sequences=stop_sequences,
        )
    else:
        raise ValueError(f"Invalid API endpoint: {api_endpoint}")

    return response

def summarize_text(text):
    conversation_history = [
        {"role": "user", "content": f"I want you to summarize as best as possible the following text: {text}"},
    ]

    genres = ["News", "Sports", "Technology", "Entertainment", "Politics", "Science", "Health", "Business", "Education", "Travel"]

    client = anthropic.Anthropic(api_key=api_key_anthropic)
    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=conversation_history
    ) as stream:
        summary = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            summary += text
        print("\n")
        conversation_history.append({"role": "assistant", "content": summary})
    
    conversation_history.append({"role": "user", "content": f"Given this list of genres: {", ".join(genres)}. Which suits the best this text ? If no genres are appropriate, give one! Avoid giving context, I want only a one word genre, I don't want to know why or whatsoever, just give a genre either one in the genres I gave you or one more appropriate from your side!! Remember I want only to see one genre nothing else."})
    with client.messages.stream(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=conversation_history
    ) as stream:
        genre = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            genre += text
        print("\n")
        conversation_history.append({"role": "assistant", "content": genre})
    return genre, summary

def ask_question(text):
    conversation_history = [
        {"role": "user", "content": f"Based on the given text {text}, I will ask you a series of questions. Please provide concise and relevant answers."},
        {"role": "assistant", "content": "Understood. Please go ahead and ask your questions based on the provided text. I'll do my best to provide relevant and concise answers."},
    ]

    while True:
        print("\n" + "-" * 50 + "\n")
        question = input("Ask a question (or type 'quit' to exit): ")
        if question.lower() == "quit":
            break

        conversation_history.append({"role": "user", "content": question})

        client = anthropic.Anthropic(api_key=api_key_anthropic)
        with client.messages.stream(
            messages=conversation_history,
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
        ) as stream:
            print("\nAssistant:", end=" ")
            assistant_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                assistant_response += text
            print("\n")
            conversation_history.append({"role": "assistant", "content": assistant_response})

    return conversation_history