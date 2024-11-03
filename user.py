import argon2
from argon2 import PasswordHasher
from db import Database

ph = PasswordHasher()
db = Database("test.db")

class User:

  def __init__(self):
    self._id = ""
    self._username = ""
    self._password = ""
    self._vaults = []

  @property
  def id(self):
    return self._id
  
  @id.setter
  def id(self, id):
    self._id = id
  
  @property
  def username(self):
    return self._username
  
  @username.setter
  def username(self, username):
    self._username = username
  
  @property
  def password(self):
    return self._password
  
  @password.setter
  def password(self, password):
    self._password = password

  @property
  def vaults(self):
    return self._vaults
  
  @vaults.setter
  def vaults(self, vaults):
   self._vaults = vaults

  def register(self, username, password):
    pw_hash = ph.hash(password)
    db.add_user(username, pw_hash)

  def login(self, username, password):
    try:
      user = db.get_user(username)
      verified = ph.verify(user["password"], password)

      if verified:
        print(f"{username} verified, logging in...")
        self.id = user["id"]
        self.username = user["username"]
        self.password = user["password"]
        self.vaults = db.get_vaults(user["id"])
        
    except TypeError:
      print("username not on file.")
    except argon2.exceptions.VerifyMismatchError:
      print("password is incorrect.")

  def add_vault(self, vault_name):
    db.add_vault(self, vault_name)
    self.vaults = db.get_vaults(self.id)






