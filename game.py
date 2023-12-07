import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS game(
    id INTEGER PRIMARY KEY,
    endgame INTEGER
)
''')
cursor.execute(''' INSERT INTO game (id,endgame) VALUES (1,0)  ''')
conn.commit()
conn.close()
