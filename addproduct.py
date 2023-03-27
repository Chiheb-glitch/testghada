import sqlite3

# Connect to the database
conn = sqlite3.connect('stdb.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Define the data to be inserted
data = ('John', 26, "test")
cursor.execute('DELETE FROM product')
# Execute the SQL statement to insert the data
cursor.execute('INSERT INTO product (name, id, image) VALUES (?, ?, ?)', data)

# Commit the transaction to save the changes to the database
conn.commit()