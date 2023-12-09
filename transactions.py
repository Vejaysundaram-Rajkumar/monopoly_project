import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE  IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    transaction_type TEXT,
    player_name TEXT,
    amount INTEGER,
    property_type TEXT,  
    specific_property TEXT,
    dice_roll INTEGER
)
''')

conn.commit()
conn.close()