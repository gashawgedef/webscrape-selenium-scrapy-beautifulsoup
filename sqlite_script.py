import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('audible_books.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table for storing scraped data
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT,
    book_author TEXT,
    narrated_by TEXT,
    series TEXT,
    book_length TEXT,
    released_date TEXT,
    language TEXT,
    ratings TEXT
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
