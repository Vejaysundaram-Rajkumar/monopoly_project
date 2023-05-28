import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT,
    current_money INTEGER
)
''')
conn.commit()
conn.close()
