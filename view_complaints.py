import sqlite3

conn = sqlite3.connect('complaints.db')
c = conn.cursor()

c.execute('SELECT * FROM complaints')
data = c.fetchall()

for row in data:
    print(row)

conn.close()