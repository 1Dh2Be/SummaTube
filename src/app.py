import os
import sys
import json
import time 

# Get the current working directory
summa_tube_path = os.getcwd()


# Add the SummaTube directory to the Python path
sys.path.append(summa_tube_path)

from database import database
import script

MENU_VIDEO_PROMPT ="""-- SummaTube App --

Please choose one of this options:

1) Enter video URL.
2) Exit.

Your selection: """

MENU_PROMPT = """-- SummaTube App -- 

Please choose one of this options:

1) Get text.
2) Summarize video.
3) Ask questions about video.
4) Exit.

Your selection: """

def menu():
    """
    Provides an interactive menu for the SummaTube application.

    This function handles user input to download a YouTube video, extract the audio, 
    convert to text, summarize, ask questions, and store results in a database.

    It establishes a connection to the SQLite database, gets the next available row id, 
    prompts the user for a YouTube URL, downloads the audio, extracts text, allows the 
    user to view the text and generate a summary and Q&A. The text, summary, and Q&A 
    are stored in the database before exiting.

    Returns:
        None: This function does not return a value.
    """
    
    connection = database.connect()
    database.create_tables(connection)

    id = database.get_last_row(connection) + 1
    
    database.add_id(connection, id)

    video_url = None
    while video_url is None:
        user_input = input(MENU_VIDEO_PROMPT)
        if user_input == "1":
            output_path = os.path.expanduser("src/audio")
            video_url = input("Enter video URL: ")
            global title
            id_video, title = script.download_audio_from_youtube(video_url, output_path)
        elif user_input == "2":
            print("Exiting the program...")
            return
        else:
            print("Please Enter a valid number!")
    
    # Converts the extracted audio to text and stores it. 
    extracted_text = script.speech_to_text(f"src/audio/{id_video}.mp3")

    while True:
        print("\n")
        user_input = input(MENU_PROMPT)
        if user_input == "1":

            print("\n", extracted_text, "\n")

            database.add_text(connection, extracted_text, id)
            time.sleep(1)

        elif user_input == "2":
            
            print("\n")
            # Summarize the text.
            genre, summary = script.summarize_text(extracted_text)

            database.add_text(connection, id, extracted_text)
            database.add_summary(connection, id, title, video_url, genre, summary)

        elif user_input == "3":

            # Gets the conversation history.  
            questions_answers_history = script.ask_question(extracted_text)

            # Formats it to json to store it in database.
            questions_answers_formatted = json.dumps(questions_answers_history, indent=2)
            
            database.add_questions_answers(connection, id, questions_answers_formatted)
            
        elif user_input == "4":
            print("Exiting the program...")
            break
        else:
            print("Please enter a valid number! ")

if __name__ == "__main__":
    menu()