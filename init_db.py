import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO Clients (father_name, mother_name, permanent_address) VALUES (?, ?, ?)",
            ('Moby-Dick', 'Herman Melville', '137 BDV AUGUSTE')
            )

cur.execute("INSERT INTO Clients (father_name, mother_name, permanent_address) VALUES (?, ?, ?)",
            ('Mick Hol', 'THANG', '1 BDV EMILE')
            )

cur.execute("INSERT INTO Clients (father_name, mother_name, permanent_address) VALUES (?, ?, ?)",
            ('BOBY POT', 'XUEE', '18 CHEMIN ROUGE')
            )

cur.execute("INSERT INTO Clients (father_name, mother_name, permanent_address) VALUES (?, ?, ?)",
            ('ZHANG THEODORE', 'LAURA RO', '118 RUE JOSEPH')
            )


connection.commit()
connection.close()
