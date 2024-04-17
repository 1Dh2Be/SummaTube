from script import *
import os 

def main():
    video_url = "https://www.youtube.com/watch?v=zcUGLp5vwaQ"
    output_path = os.path.expanduser("src/audio")

    # Extracts the audio from a youtube video.
    title = download_audio_from_youtube(video_url, output_path)

    # Converts the extracted audio to text and stores it. 
    extracted_text = speech_to_text(f"src/audio/{title}.mp3")

    # Summarize the text.
    summary = summarize_text(extracted_text)

    # Saves the summarized text to a txt file
    save_output_to_txt(summary, title)

if __name__ == "__main__":
    main()