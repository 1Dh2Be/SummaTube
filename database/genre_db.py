import sqlite3
import os

current_dir = os.getcwd()

CREATE_GENRES_TABLE = "CREATE TABLE IF NOT EXISTS genres (ID_Genre INTEGER PRIMARY KEY, genre TEXT);"

INSERT_GENRE = "INSERT INTO genres (genre) VALUES (?);"

INSERT_ID = "INSERT INTO genres (ID_Genre) VALUES (?);"

GET_GENRES = "SELECT genre FROM genres;"

def connect():

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the SummaTube.db file
    db_path = os.path.join(script_dir, 'genres.db')

    return sqlite3.connect(db_path)

def create_tables(connection):
    with connection:
        connection.execute(CREATE_GENRES_TABLE)

def get_genres(connection):
    with connection:
        genres = connection.execute(GET_GENRES).fetchall()
        list_genres = []
        for genre in genres:
            list_genres.append(genre[0])
        return list_genres
    
def add_genre(connection, genre):
    with connection:
        connection.execute(INSERT_GENRE, (genre,))


def add_id(connection, id):
    with connection:
        connection.execute(INSERT_ID, (id,))




