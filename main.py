from db import Database
from user import User

db = Database("test.db")
db.generate_tables()
user = User()

while True:
  option = input("1. Register New Account\n2. Log In\n3. Reset Password\n")
  if option == "1":
    print("----REGISTRATION----")
    username = input("Please enter your username:")
    password = input("Please enter your password:")
    user.register(username, password)
  if option == "2":
    print("----LOG IN----")
    username = input("Please enter your username:")
    password = input("Please enter your password:")
    verified = user.login(username, password)
    if verified:
      option = input("1. Add Vault\n")
      if option == "1":
        print("----ADD VAULT----")
        name = input("Please enter vault name:")
        user.add_vault(name)
  if option == "3":
    print("----RESET PASSWORD----")
    username = input("Please enter your username:")
    password = input("Please enter your password:")
    verified = user.login(username, password)
    if verified:
      print("----RESET PASSWORD----")
      new_pw = input("Please enter new password:")
      user.change_password(new_pw)


