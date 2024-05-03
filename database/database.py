import os
import sqlite3

CREATE_VIDEO_SUMMARIES_TABLE = "CREATE TABLE IF NOT EXISTS video_summaries (id INTEGER PRIMARY KEY, title TEXT, url TEXT, genre TEXT, text TEXT, summary TEXT, questions_answers TEXT)"

INSERT_SUMMARIZATION = "UPDATE video_summaries SET title = ?, url = ?, genre = ?, summary = ? WHERE id = ?;"

INSERT_QUESTIONS = "UPDATE video_summaries SET questions_answers = ? WHERE id = ?;"

INSERT_TEXT = "UPDATE OR IGNORE video_summaries SET text = ? WHERE id = ?;"

INSERT_ID = "INSERT INTO video_summaries (id) VALUES (?);"

FIND_LAST_ROW = "SELECT id FROM video_summaries ORDER BY id DESC LIMIT 1;"

def connect():

     # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the database directory
    database_dir = os.path.join(script_dir, '..', 'database')

    # Construct the path to the SummaTube.db file
    db_path = os.path.join(database_dir, 'SummaTube.db')

    # Connect to the database
    return sqlite3.connect(db_path)

def create_tables(connection):
    with connection:
        connection.execute(CREATE_VIDEO_SUMMARIES_TABLE)

def add_summary(connection, id, title, url, genre, summary):
    with connection:
        connection.execute(INSERT_SUMMARIZATION, (title, url, genre, summary, id,))

def add_questions_answers(connection, id, questions_answers):
    with connection:
        connection.execute(INSERT_QUESTIONS, (questions_answers, id,))

def add_text(connection, id,  text):
    with connection:
        connection.execute(INSERT_TEXT, (text, id,))

def add_id(connection, id):
    with connection:
        connection.execute(INSERT_ID, (id,))

def get_last_row(connection):
    with connection:
        id = connection.execute(FIND_LAST_ROW).fetchone()
        return id[0]