import sqlite3
from flask import request, flash, url_for, redirect
from prettytable import PrettyTable

class Database:
    EMPLOYEES_COLUMNS = {
        'id': 'INTEGER PRIMARY KEY UNIQUE',
        'first_name': 'TEXT NOT NULL',
        'last_name': 'TEXT NOT NULL',
        'password': 'TEXT',
        'email': 'TEXT NOT NULL UNIQUE',
    }

    CLIENTS_COLUMNS = {
        'id': 'INTEGER PRIMARY KEY UNIQUE',
        'first_name': 'TEXT NOT NULL',
        'last_name': 'TEXT NOT NULL',
    }

    TABLES_COLUMNS = {
        'employees': EMPLOYEES_COLUMNS,
        'clients': CLIENTS_COLUMNS
    }

    def __init__(self, db_name='company.db'): # The location of where the db is can be changed.
        """Establish a single connection during object initialization"""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Database Connection establish")

    def _execute_query(self, query, params=()):
        """General method for executing queries to avoid repetition"""
        try:
            self.cursor.execute(query,params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during query execution: {e}")
            raise

    def create_table(self, table_name):
        """Create a table if it doesn't exist."""
        columns = self.TABLES_COLUMNS.get(table_name.lower())
        if not columns: #if table_name is not 'employees'/'clients' columns will be None.
            print (f"Invalid table name '{table_name}'")
            return

        #Checks if a table with the given name exists.
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")

        #if not exists - create one.
        if not self.cursor.fetchone():
            columns_definition = ', '.join(f'{col} {dtype}' for col, dtype in columns.items())
            create_table_query = f"CREATE TABLE {table_name} ({columns_definition});"
            self._execute_query(create_table_query)
            print(f"Table '{table_name}' created successfully.")

    def insert_user_to_table(self, table_name, user_data):
        """Insert user data into a specific table"""
        try:
            columns = ', '.join(user_data.keys())
            placeholders = ', '.join(['?' for _ in user_data]) # create a string of placeholders
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            #tuple(user_data.values()) - Converts the dictionary values into a tuple to bind the data to the placeholders.
            self._execute_query(query,tuple(user_data.values()))
        except sqlite3.IntegrityError as e:
            # Handle specific database integrity errors (like UNIQUE constraint failure)
            print(f"Error inserting user into '{table_name}': {e}")
            return
        except sqlite3.Error as e:
            # Handle other SQLite-related errors
            print(f"Database error inserting user into '{table_name}': {e}")
            return
        print(f"User inserted into '{table_name}' successfully.")

    def print_table(self, table_name):
        """Print all rows from a specified table"""
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            if rows:
                self.cursor.execute(f"PRAGMA table_info('{table_name}')") #returns metadata about the columns in the table
                columns_name = [info[1] for info in self.cursor.fetchall()]
                table = PrettyTable()
                table.field_names = columns_name
                for row in rows:
                    table.add_row(row)
                print(f"\nContents of table '{table_name}':")
                print(table)
            else:
                print(f"Table '{table_name}' is empty.")
        except sqlite3.Error as e:
            print(f"Error reading table '{table_name}': {e}")

    def change_password(self, email, old_password, new_password, table_name='employees'):
        """Update the password for a specified user"""
        try:
            self.cursor.execute(f"SELECT password FROM {table_name} WHERE email = '{email}'")
            stored_password = self.cursor.fetchone()
            if stored_password:
                self._execute_query(f"UPDATE {table_name} SET password = '{new_password}' WHERE email = '{email}'")
                print(f"Password for user '{email}' updated successfully in '{table_name}' table.")
            else:
                print(f"Invalid old password or email for {email}")
        except sqlite3.Error as e:
            print(f"Error updating password for user in '{table_name}': {e}")

    def validate_user_login(self, email, password):
        """Validate the user's email and password"""
        self.cursor.execute(f"SELECT password FROM employees WHERE email = '{email}'")
        stored_password = self.cursor.fetchone() #fetchone command get the password as tuple
        if stored_password:
            stored_password = stored_password[0] # Extract the password from the tuple.
        if stored_password == password:
            print("Successfully validate user's info.")
            return True
        else:
            print("Invalid email or password - during validate-user.")
            return False

    def fetch_user_data_from_register_page(self):
        """Fetch user data from the 'register' page form."""
        email = request.form.get('email')
        user_id = request.form.get('id')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            print("Pasaswords did not matched -- got redirected to register")
            return redirect(url_for('register'))

        return {
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'password': password1,
            'email': email,
        }

    def fetch_user_data_from_add_clients_page(self):
        """Fetch user data from the addClients page form"""
        user_id = request.form.get('id')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')

        return {
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
        }

    def fetch_data_from_a_page(self, page):
        """Fetch data depending on the page"""
        if page == 'register':
            return self.fetch_user_data_from_register_page()
        elif page == 'addClients':
            return self.fetch_user_data_from_add_clients_page()
        else:
            return None

    def close(self):
        """Close the database connection"""
        self.conn.close()
