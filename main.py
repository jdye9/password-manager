from db import Database
from user import User

db = Database("test.db")
db.generate_tables()
user = User()

while True:
  print("----REGISTRATION----")
  username = input("Please enter your username:")
  password = input("Please enter your password:")
  user.register(username, password)

  print("----LOGIN----")
  username = input("Please enter your username:")
  password = input("Please enter your password:")
  user.login(username, password)

  print("----LOGIN----")
  username = input("Please enter your username:")
  password = input("Please enter your password:")
  user.login(username, password)


