import sqlite3
from argon2 import PasswordHasher
import utils

ph = PasswordHasher()
class Database:
    def __init__(self, name: 'str'):
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
                            vault_name TEXT NOT NULL UNIQUE,
                            vault_key TEXT,
                            salt TEXT,
                            nonce TEXT,
                            tag TEXT
                        )""")
      
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS logins (
                            id INTEGER PRIMARY KEY,
                            vault_id INTEGER NOT NULL,
                            domain TEXT
                            username TEXT,
                            password TEXT,
                            salt TEXT
                        )""")
        # Commit the changes
        self.commit()
      except Exception as err:
        self.close()
        raise Exception("Error connecting to database.", err)
      
    def commit(self):
      self.connection.commit()

    def close(self, commit=True):
      if commit:
        self.commit()
      self.connection.close()

    def execute(self, sql: 'str', params=None):
      self.cursor.execute(sql, params or ())

    def fetchall(self):
      return self.cursor.fetchall()

    def fetchone(self):
      return self.cursor.fetchone()

    def query(self, sql: 'str', params=None):
      self.cursor.execute(sql, params or ())
      return self.fetchall()
    
    def get_user(self, username: 'str'):
      try:
        user = self.query("SELECT * FROM users WHERE username = ?", (username,))
        user = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, user))
        return user[0] if len(user) else None
      except Exception as err:
        raise Exception("Error fetching users.", err)
    
    def get_users(self):
      try:
        users = self.query("SELECT * FROM users")
        users = list(map(lambda x: {"id": x["id"], "username": x["username"], "password": x["password"]}, users))
        return users
      except Exception as err:
        raise Exception("Error fetching vaults.", err)
    
    def get_vaults(self, user_id: 'str'):
      try:
        vaults = self.query("SELECT * FROM vaults WHERE user_id = ?", (user_id,))
        vaults = list(map(lambda x: {"id": x["id"], "user_id": x["user_id"], "vault_name": x["vault_name"], "vault_key": x["vault_key"], "salt": x["salt"], "nonce": x["nonce"], "tag": x["tag"]}, vaults))
        return vaults
      except Exception as err:
        raise Exception("Error fetching vaults.", err)

    def add_user(self, username: 'str', password: 'str'):
      try:
        users = list(map(lambda x: x["username"].lower(), self.get_users()))
        if username.lower() not in users:
          self.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
          self.commit()
          print(f"{username} added successfully.")
        else:
          raise Exception(f"{username} already exists.")
      except Exception as err:
        raise Exception("Error occurred while trying to add user.", err)

    def add_vault(self, user: 'User', vault_name: 'str'):
      try:
        vaults = list(map(lambda x: x["vault_name"].lower(), self.get_vaults(user.id)))
        if vault_name.lower() not in vaults:
            # generate random 256 bit vault key
            vault_key = utils.generate_vault_key()
            # encrypt vault key
            enc_vault_key = utils.encrypt(vault_key, user.password)
            self.execute('INSERT INTO vaults (user_id, vault_name, vault_key, salt, nonce, tag) VALUES (?, ?, ?, ?, ?, ?)', (user.id, vault_name, enc_vault_key["cipher_text"], enc_vault_key["salt"], enc_vault_key["nonce"], enc_vault_key["tag"]))
            self.commit()
            user.vaults = self.get_vaults(user.id)
            print(f"{vault_name} added successfully.")
        else:
          raise Exception(f"{vault_name} already exists.")
      except Exception as err:
        raise Exception("Error occurred while trying to create new vault.", err)
    
    def edit_user_password(self, user: 'User', new_password: 'str', vault_changes: 'list[dict]'):
      try:
        users = list(map(lambda x: x["id"], self.get_users()))
        if user.id in users:
          for vault_change in vault_changes:
            print(vault_change)
            self.execute('UPDATE vaults SET vault_key = ?, salt = ?, nonce = ?, tag = ? WHERE id = ?;', (vault_change["cipher_text"], vault_change["salt"], vault_change["nonce"], vault_change["tag"], vault_change["id"]))
          print("HERE")
          hash = ph.hash(new_password)
          self.execute('UPDATE users SET password = ? WHERE id = ?;', (hash, user.id))
          self.commit()
          self.password = new_password
          self.vaults = self.get_vaults(user.id)
          print(f"Password for {user.username} changed successfully. Vault key encryption updated.")
        else:
          raise Exception(f"User not found.")
      except Exception as err:
        raise Exception("Error occurred while updating password.", err)