import sqlite3
import os

current_dir = os.getcwd()

CREATE_GENRES_TABLE = "CREATE TABLE IF NOT EXISTS genres (ID_Genre INTEGER PRIMARY KEY, genre TEXT);"

INSERT_GENRE = "INSERT INTO genres (genre) VALUES (?);"

INSERT_ID = "INSERT INTO genres (ID_Genre) VALUES (?);"

GET_GENRES = "SELECT genre FROM genres;"

def connect():
    """
    Establishes and returns a connection to the genres database.

    This function constructs the path to the 'genres.db' database file based on the current script's directory,
    and then establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the genres database.
    """

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the SummaTube.db file
    db_path = os.path.join(script_dir, 'genres.db')

    return sqlite3.connect(db_path)

def create_tables(connection):
    """
    Creates the genres table in the database if it does not already exist.

    Parameters:
        connection (sqlite3.Connection): The database connection object.

    Returns:
        None: This function does not return a value but creates a table in the database.
    """

    with connection:
        connection.execute(CREATE_GENRES_TABLE)

def get_genres(connection):
    """
    Retrieves all genres from the genres table.

    Parameters:
        connection (sqlite3.Connection): The database connection object.

    Returns:
        list: A list of genre names stored in the database.
    """
        
    with connection:
        genres = connection.execute(GET_GENRES).fetchall()
        list_genres = []
        for genre in genres:
            list_genres.append(genre[0])
        return list_genres
    
def add_genre(connection, genre):
    """
    Adds a new genre to the genres table.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        genre (str): The name of the genre to add.

    Returns:
        None: This function does not return a value but inserts a new genre into the database.
    """

    with connection:
        connection.execute(INSERT_GENRE, (genre,))


def add_id(connection, id):
    """
    Adds a new row with the specified ID to the genres table.

    Parameters:
        connection (sqlite3.Connection): The database connection object.
        id (int): The ID to add.

    Returns:
        None: This function does not return a value but inserts a new ID into the database.
    """
        
    with connection:
        connection.execute(INSERT_ID, (id,))




