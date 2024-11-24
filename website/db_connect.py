import sqlite3 


conn = sqlite3.connect('database.db')
print("connected to database successfully")


conn.close()
