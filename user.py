import argon2
from argon2 import PasswordHasher
from db import Database

ph = PasswordHasher()
db = Database("test.db")

class User:

  def __init__(self):
    self._username = ""
    self._password = ""

  @property
  def username(self):
    return self._username
  
  @property
  def set_username(self, username):
    self._username = username
  
  @property
  def password(self):
    return self._password
  
  @property
  def set_password(self, password):
    self._password = password

  def register(self, username, password):
    pw_hash = ph.hash(password)
    db.add_new_user(username, pw_hash)

  def login(self, username, password):
    try:
      existingUser = db.get_existing_user(username)
      verified = ph.verify(existingUser["password"], password)

      if verified:
        print(f"{username} verified, logging in...")
        self.set_username(username)
        self.set_password(password)
    
    except TypeError:
      print("username not on file.")
    except argon2.exceptions.VerifyMismatchError:
      print("password is incorrect.")





