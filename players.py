import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    name TEXT,
    current_money INTEGER,
    game_name TEXT,
    spent_property INTEGER DEFAULT 0,
    spent_construction INTEGER DEFAULT 0,
    spent_rent INTEGER DEFAULT 0,
    other_spendings INTEGER DEFAULT 0,
    gained_rent INTEGER DEFAULT 0,
    other_gains INTEGER DEFAULT 0
)
''')
conn.commit()
conn.close()
