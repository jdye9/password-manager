import sqlite3
from argon2 import PasswordHasher
import utils

ph = PasswordHasher()
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
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )""")
      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS vaults (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            vault_name TEXT UNIQUE,
                            vault_key TEXT,
                            salt TEXT,
                            nonce TEXT,
                            tag TEXT
                        )""")
      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS logins (
                            id INTEGER PRIMARY KEY,
                            vault_id INTEGER NOT NULL,
                            domain: TEXT
                            username TEXT,
                            password TEXT,
                            salt TEXT
                        )""")
        # Commit the changes
        self.commit()
      except:
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
    
    def get_user(self, username):
      user = self.query("SELECT * FROM users WHERE username = ?", (username,))
      user = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, user))
      return user[0] if len(user) else None
    
    def get_users(self):
      users = self.query("SELECT * FROM users")
      users = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, users))
      return users
    
    def get_vaults(self, user_id):
      vaults = self.query("SELECT * FROM vaults WHERE user_id = ?", (user_id,))
      vaults = list(map(lambda x: {"id": x["id"], "user_id": x["user_id"], "vault_key": x["vault_key"], "vault_name": x["vault_name"], "salt": x["salt"]}, vaults))
      return vaults

    def add_user(self, username, password):
      users = list(map(lambda x: x["username"], self.get_users()))
      if username not in users:
        self.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.commit()
        print(f"{username} added successfully.")
      else:
        print(f"{username} already exists.")

    def add_vault(self, user, vault_name):
      vaults = list(map(lambda x: x["vault_name"], self.get_vaults(user.id)))
      if vault_name not in vaults:
        vault_key = utils.generate_vault_key()
        print(vault_key)
        enc_vault_key = utils.encrypt(vault_key, user.password)
        print(enc_vault_key)
        self.execute('INSERT INTO vaults (user_id, vault_name, vault_key, salt, nonce, tag) VALUES (?, ?, ?, ?, ?, ?)', (user.id, vault_name, enc_vault_key["cipher_text"], enc_vault_key["salt"], enc_vault_key["nonce"], enc_vault_key["tag"]))
        self.commit()
        print(f"{vault_name} added successfully.")
      else:
        print(f"{vault_name} already exists.")