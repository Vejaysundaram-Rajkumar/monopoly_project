import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS trains (
    id INTEGER PRIMARY KEY,
    name TEXT,
    group_id INTEGER,
    purchase_price INTEGER,
    mortgage_value INTEGER,
    rent_1T INTEGER,
    rent_2T INTEGER,
    rent_3T INTEGER,
    rent_4T INTEGER,
    Owner TEXT,
    current_rate TEXT
)
''')
cursor.execute('''
INSERT INTO trains (id, name, group_id, purchase_price, mortgage_value, rent_1T, rent_2T, rent_3T, rent_4T,Owner,current_rate)
VALUES 
    (1, 'Marylebone Station', 10, 2000000, 1000000, 250000, 500000, 1000000, 2000000,'bank','rent_1T'),
    (2, 'King Cross Station', 10, 2000000, 1000000, 250000, 500000, 1000000, 2000000,'bank','rent_1T'),
    (3, 'Liverpool Street Station', 10, 2000000, 1000000, 250000, 500000, 1000000, 2000000,'bank','rent_1T'),
    (4, 'Fenchurch Street Station', 10, 2000000, 1000000, 250000, 500000, 1000000, 2000000,'bank','rent_1T')
    ''')

conn.commit()
conn.close()
