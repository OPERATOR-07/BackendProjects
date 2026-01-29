import sqlite3 as db

try:
    conn = db.connect("Mydatabase.db")
    cursor = conn.cursor()
    
    cursor.execute("""create table Users(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT UNIQUE,
            Password TEXT
        );""")
    conn.commit()
    print("Database created")
    
except db.Error as error:
    print(f"Error: {error}")
