import argon2
from argon2 import PasswordHasher
from data_classes.db import Database

ph = PasswordHasher()
db = Database("test.db")


class Credentials:

    def register(self, username, password):
        try:
            pw_hash = ph.hash(password)
            db.add_user(username, pw_hash)
            return True
        except Exception as err:
            print("Error registering account.", err)
            return False

    def login(self, username, password):
        try:
            user = db.get_user(username)
            verified = ph.verify(user["password"], password)

            if verified:
                print(f"{username} verified, logging in...")
                self.id = user["id"]
                self.username = user["username"]
                self.password = password
                self.vaults = db.get_vaults(user["id"])
                return True

        except TypeError as err:
            print("username not on file.", err)
            return False
        except argon2.exceptions.VerifyMismatchError as err:
            print("password is incorrect.", err)
            return False
