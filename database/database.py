import os
import sqlite3

CREATE_VIDEO_SUMMARIES_TABLE = "CREATE TABLE IF NOT EXISTS video_summaries (id INTEGER PRIMARY KEY, title TEXT, url TEXT, genre TEXT, text TEXT, summary TEXT, questions_answers TEXT)"

INSERT_SUMMARIZATION = "UPDATE video_summaries SET title = ?, url = ?, genre = ?, summary = ? WHERE id = ?;"

INSERT_QUESTIONS = "UPDATE video_summaries SET questions_answers = ? WHERE id = ?;"

INSERT_TEXT = "UPDATE OR IGNORE video_summaries SET text = ? WHERE id = ?;"

INSERT_ID = "INSERT INTO video_summaries (id) VALUES (?);"

FIND_LAST_ROW = "SELECT id FROM video_summaries ORDER BY id DESC LIMIT 1;"

def connect():
    """
    Establishes and returns a connection to the SummaTube database.

    This function constructs the path to the 'SummaTube.db' database file based on the current script's directory,
    and then establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the SummaTube database.

    Example:
        conn = connect()
        print("Database connection established.")
    """

     # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the database directory
    database_dir = os.path.join(script_dir, '..', 'database')

    # Construct the path to the SummaTube.db file
    db_path = os.path.join(database_dir, 'SummaTube.db')

    # Connect to the database
    return sqlite3.connect(db_path)

def create_tables(connection):
    """
    Creates the video summaries table in the database if it does not already exist.

    Parameters:
        connection (sqlite3.Connection): The database connection object.

    Returns:
        None: This function does not return a value but creates a table in the database.

    Example:
        conn = sqlite3.connect('example.db')
        create_tables(conn)
    """

    with connection:
        connection.execute(CREATE_VIDEO_SUMMARIES_TABLE)

def add_summary(connection, id, title, url, genre, summary):
    """
    Saves the summary of a video in the database.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        id (int): The unique identifier for the video.
        title (str): The title of the video.
        url (str): The URL where the video can be accessed.
        genre (str): The genre of the video.
        summary (str): A text summary of the video content.

    Returns:
        None: This function does not return a value but updates the database.

    Example:
        conn = sqlite3.connect('example.db')
        add_summary(conn, 101, "Sample Video", "http://example.com", "Education", "This is a summary.")
    """

    with connection:
        connection.execute(INSERT_SUMMARIZATION, (title, url, genre, summary, id,))

def add_questions_answers(connection, id, questions_answers):
    """
    Saves the questions and answers related to a video in the database.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        id (int): The unique identifier for the video.
        questions_answers (str): The JSON string containing questions and answers.

    Returns:
        None: This function does not return a value but updates the database.

    Example:
        conn = sqlite3.connect('example.db')
        add_questions_answers(conn, 101, '{"What is the main topic?": "Science"}')
    """

    with connection:
        connection.execute(INSERT_QUESTIONS, (questions_answers, id,))

def add_text(connection, id,  text):
    """
    Saves the text of the video to the database.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        id (int): The unique identifier for the video.
        text (str): The extracted text from the video.

    Returns:
        None: This function does not return a value but updates the database.

    Example:
        conn = sqlite3.connect('example.db')
        add_text(conn, 101, "Here is some example text from the video.")
    """

    with connection:
        connection.execute(INSERT_TEXT, (text, id,))


def get_last_row(connection):
    """
    Retrieves the last row id from the video summaries table.

    Parameters:
        connection (sqlite3.Connection): The database connection object.

    Returns:
        int: The id of the last row in the video summaries table.

    Example:
        conn = sqlite3.connect('example.db')
        last_id = get_last_row(conn)
        print(f"Last row id: {last_id}")
    """

    with connection:
        id = connection.execute(FIND_LAST_ROW).fetchone()
        return id[0]
    
def add_id(connection, id):
    """
    Creates a new row with the given id in the video summaries table.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        id (int): The unique identifier for the new row.

    Returns:
        None: This function does not return a value but inserts a new row in the database.

    Example:
        conn = sqlite3.connect('example.db')
        add_id(conn, 102)
    """
    
    with connection:
        connection.execute(INSERT_ID, (id,))