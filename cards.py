import sqlite3

conn = sqlite3.connect('gamedetails.db')

cursor = conn.cursor()

# Create the "cards" table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        Id INTEGER PRIMARY KEY,
        Statement TEXT,
        Amount INTEGER,
        Option TEXT
    )
''')

# Insert values into the "cards" table
card_values = [
    (1, 'Advance to Go (Collect 2M)', 2000000, 'community chest'),
    (2, 'Bank error in your favour Collect 2M', 2000000, 'community chest'),
    (3, 'From sale of stock you get 50K', 50000, 'community chest'),
    (4, 'Holiday fund matures Receive 100K', 100000, 'community chest'),
    (5, 'It is your birthday Collect 100k from every player', 100000, 'community chest'),
    (6, 'Life insurance matures Collect 100K', 100000, 'community chest'),
    (7, 'Receive 250K consultancy fee', 250000, 'community chest'),
    (8, 'You have won second prize in a beauty contest Collect 100K', 100000, 'community chest'),
    (9, 'Advance to Go (Collect 2M)', 2000000, 'chance'),
    (10, 'Your building loan matures Collect 150K', 150000, 'chance'),
    (11, 'Bank pays you dividend of 50K', 50000, 'chance'),
    (12, 'Make general repairs on all your property For each house pay 250K For each hotel pay 100K', None, 'chance'),
    (13,'You have been elected Chairman of the Board. Collect 150K.' , 150000, 'chance'),
    (14, 'Speeding fine 150K', 150000, 'chance'),
    (15, 'You are assessed for street repairs 140K per house 215K per hotel', None, 'community chest'),
    (16, 'You cheated the bank by giving wrong name pay fine of 100K', 100000, 'community chest'),
    (17, 'Income tax fraud pay 120K', 120000, 'community chest'),
    (18, "Doctor's fee Pay 50K", 50000, 'community chest'),
    (19, 'Pay hospital fees of 100K', 100000, 'community chest'),
    (20, 'Pay school fees of 150K', 150000, 'community chest'),
    (21, 'Advance to the nearest Station If unowned, you may buy it from the Bank If owned, pay owner twice the rental', None, 'chance'),
    (22, 'Advance to the nearest Station If unowned, you may buy it from the Bank If owned, pay owner twice the rental', None, 'chance'),
    (23, 'Advance token to nearest Utility If unowned, you may buy it from the Bank If owned, throw dice and pay owner a total ten times amount thrown', None, 'chance'),
    (24, 'Go to Jail Go directly to jail, do not pass Go, do not collect 2M', None, 'community chest'),
    (25, 'Advance to Trafalgar Square If you pass Go, collect 2M', None, 'chance'),
    (26, 'Advance to Mayfair', None, 'chance'),
    (27, 'Advance to Pall Mall If you pass Go, collect 2M', None, 'chance'),
    (28, 'Take a trip to Kings Cross Station If you pass Go, collect 2M', None, 'chance'),
    (29, 'Go Back 3 Spaces', None, 'chance'),
    (30, 'Go to Jail Go directly to Jail, do not pass Go, do not collect 2M', None, 'chance'),
    (31, 'Get Out of Jail Free', None, 'chance'),
    (32, 'Get Out of Jail Free', None, 'community chest'),
]

cursor.executemany('INSERT INTO cards (Id, Statement, Amount, Option) VALUES (?, ?, ?, ?)', card_values)

# Commit the changes and close the connection
conn.commit()
conn.close()
