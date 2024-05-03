import os
import sys
import yt_dlp as youtube_dl
import assemblyai as aai
import anthropic
from api_keys import ASSEMBLYAI_API_KEY, ANTHROPIC_API_KEY

current_path = os.getcwd()

sys.path.append(current_path)

from database import genre_db

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
        id = info['id']
        title = info['title']
        print(f"Audio downloaded from {video_url} and saved as {id}")
    return id, title

def speech_to_text(file):
    aai.settings.api_key = ASSEMBLYAI_API_KEY
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    text = transcript.text
    os.remove(file)
    return text

def get_completion(conversation_history, question: bool = True):
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    if question:
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
            return assistant_response
    else:
        with client.messages.stream(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=conversation_history
        ) as stream:
            response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response += text
            print("\n")
            return response

def summarize_text(text):
    conn = genre_db.connect()
    genres = genre_db.get_genres(conn)

    conversation_history = [
        {"role": "user", "content": f"I want you to summarize as best as possible the following text: {text}"},
    ]

    summary = get_completion(conversation_history, question=False)
    conversation_history.append({"role": "assistant", "content": summary})


    conversation_history.append({"role": "user", "content": f"Given this list of genres: {", ".join(genres)}. Which suits the best this text ? If no genres are appropriate, give one! Avoid giving context, I want only a one word genre, I don't want to know why or whatsoever, just give a genre either one in the genres I gave you or one more appropriate from your side!! Remember I want only to see one genre nothing else."})
    
    genre = get_completion(conversation_history, question=False)
    conversation_history.append({"role": "assistant", "content": genre})

    if genre not in genres:
        genre_db.add_genre(conn, genre)
    else:
        pass

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

        assistant_response = get_completion(conversation_history)
        conversation_history.append({"role": "assistant", "content": assistant_response})

    return conversation_history