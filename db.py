import sqlite3

class Database:
    def __init__(self, name):
      self._conn = sqlite3.connect(name)
      self._conn.row_factory = sqlite3.Row
      self._cursor = self._conn.cursor()

    def __enter__(self):
      return self

    def __exit__(self, exc_type, exc_val, exc_tb):
      self.close()

    @property
    def connection(self):
      return self._conn

    @property
    def cursor(self):
      return self._cursor
    
    def generate_tables(self):
      try:
      # Create a table (if it doesn't exist)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT
                        )""")
      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS vaults (
                            id INTEGER PRIMARY KEY,
                            userId INTEGER,
                            vaultKey TEXT,
                            vaultName TEXT,
                            salt TEXT
                        )""")
      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS logins (
                            id INTEGER PRIMARY KEY,
                            vaultId INTEGER,
                            username TEXT,
                            password TEXT,
                            salt TEXT
                        )""")
        # Commit the changes
        self.commit()
      except e:
        print("Error connecting to database.")
        self.close()
      
    def commit(self):
      self.connection.commit()

    def close(self, commit=True):
      if commit:
        self.commit()
      self.connection.close()

    def execute(self, sql, params=None):
      self.cursor.execute(sql, params or ())

    def fetchall(self):
      return self.cursor.fetchall()

    def fetchone(self):
      return self.cursor.fetchone()

    def query(self, sql, params=None):
      self.cursor.execute(sql, params or ())
      return self.fetchall()
    
    def get_existing_user(self, username):
      existingUser = self.query("SELECT * FROM users WHERE username = ?", (username,))
      existingUser = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, existingUser))
      return existingUser[0] if len(existingUser) else None
    
    def get_existing_users(self):
      existingUsers = self.query("SELECT * FROM users")
      existingUsers = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, existingUsers))
      return existingUsers

    def add_new_user(self, username, password):
      existingUsernames = list(map(lambda x: x["username"], self.get_existing_users()))
      if username not in existingUsernames:
        print(f"{username} added successfully.")
        self.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.commit()
      else:
        print(f"{username} already exists.")