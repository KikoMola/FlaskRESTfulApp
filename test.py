import sqlite3

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

users = [
    (1, 'Kiko', '1111'),
    (2, 'Sherly', '2222'),
    (3, 'Carlos', '3333')
]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()