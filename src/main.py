from script import *
import os 
def main():
    video_url = "https://www.youtube.com/watch?v=_lMpneeo438"
    output_path = os.path.expanduser("src/audio")

    # Extracts the audio from a youtube video.
    download_audio_from_youtube(video_url, output_path)

    # Converts the extracted audio to text and stores it. 
    text = speech_to_text("src/audio/audio.mp3")

    # summarize the text.
    summarize_text(text)
    
if __name__ == "__main__":
    main()