import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS utilities (
    id INTEGER PRIMARY KEY,
    name TEXT,
    group_id INTEGER,
    purchase_price INTEGER,
    mortgage_value INTEGER,
    rent_multiplier_1 INTEGER,
    rent_multiplier_2 INTEGER
)
''')
cursor.execute('''
INSERT INTO utilities (id, name, group_id, purchase_price, mortgage_value, rent_multiplier_1, rent_multiplier_2)
VALUES 
    (1, 'Electric Company', 9, 1500000, 750000, 4, 10),
    (2, 'Water Works', 9, 1500000, 750000, 4, 10)
''')


conn.commit()
conn.close()
