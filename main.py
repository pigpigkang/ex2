import sqlite3
import os

# Function to check if the database file exists
def database_exists():
    return os.path.exists("stephen_king_adaptations.db")

# Function to create the SQLite database and table
def create_database_and_table():
    if not database_exists():
        connection = sqlite3.connect("stephen_king_adaptations.db")
        cursor = connection.cursor()

        # Create the table without the PRIMARY KEY constraint
        cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                          movieID TEXT,
                          movieName TEXT,
                          movieYear INTEGER,
                          imdbRating REAL
                        )''')

        connection.commit()
        connection.close()

# Function to insert data into the table
def insert_data_into_table(data):
    connection = sqlite3.connect("stephen_king_adaptations.db")
    cursor = connection.cursor()

    for row in data:
        cursor.execute('INSERT OR IGNORE INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)', row)

    connection.commit()
    connection.close()

# Function to search for movies based on user's choice
def search_movies():
    while True:
        print("\nSearch options:")
        print("1. Search by movie name")
        print("2. Search by movie year")
        print("3. Search by movie rating")
        print("4. STOP")

        choice = input("Enter your choice: ")

        if choice == "1":
            movie_name = input("Enter the movie name: ")
            search_movie_by_name(movie_name)
        elif choice == "2":
            movie_year = input("Enter the movie year: ")
            search_movie_by_year(movie_year)
        elif choice == "3":
            rating_limit = input("Enter the minimum rating: ")
            search_movie_by_rating(rating_limit)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Function to search for movies by name
def search_movie_by_name(movie_name):
    connection = sqlite3.connect("stephen_king_adaptations.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?', ('%' + movie_name + '%',))
    movies = cursor.fetchall()

    connection.close()

    if movies:
        print("\nMovies found:")
        for movie in movies:
            print(f"Movie ID: {movie[0]}, Movie Name: {movie[1]}, Year: {movie[2]}, IMDB Rating: {movie[3]}")
    else:
        print("No such movie exists in our database")

# Function to search for movies by year
def search_movie_by_year(movie_year):
    connection = sqlite3.connect("stephen_king_adaptations.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?', (movie_year,))
    movies = cursor.fetchall()

    connection.close()

    if movies:
        print("\nMovies found:")
        for movie in movies:
            print(f"Movie ID: {movie[0]}, Movie Name: {movie[1]}, Year: {movie[2]}, IMDB Rating: {movie[3]}")
    else:
        print("No movies were found for that year in our database.")

# Function to search for movies by rating
def search_movie_by_rating(rating_limit):
    connection = sqlite3.connect("stephen_king_adaptations.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?', (rating_limit,))
    movies = cursor.fetchall()

    connection.close()

    if movies:
        print("\nMovies found:")
        for movie in movies:
            print(f"Movie ID: {movie[0]}, Movie Name: {movie[1]}, Year: {movie[2]}, IMDB Rating: {movie[3]}")
    else:
        print(f"No movies at or above {rating_limit} rating were found in the database.")

# Read data from the file into a list
stephen_king_adaptations_list = []
with open('stephen_king_adaptations.txt', 'r') as file:
    for line in file:
        movie_data = line.strip().split(',')
        stephen_king_adaptations_list.append((movie_data[0], movie_data[1], int(movie_data[2]), float(movie_data[3])))

# Create the database and table only if it doesn't exist
create_database_and_table()

# Insert data into the table, skipping duplicates
insert_data_into_table(stephen_king_adaptations_list)

# Start the search loop
search_movies()
