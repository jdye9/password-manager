import argon2
from argon2 import PasswordHasher
from data_classes.db import Database
from data_classes.cryptography import Cryptography

ph = PasswordHasher()
db = Database("test.db")
cryptography = Cryptography()


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
        try:
            pw_hash = ph.hash(password)
            db.add_user(username, pw_hash)
        except Exception as err:
            print("Error registering account.", err)

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

    # TODO: make sure all password resets are being done at the correct times (handle errors)
    def change_password(self, new_password):
        # when master password is changed, we must re-encrypt vault keys
        # [{id: "", vault_key: ""}]
        vault_changes = []
        for vault in self.vaults:
            dec_vault_key = cryptography.decrypt(
                {"cipher_text": vault["vault_key"], "salt": vault["salt"], "nonce": vault["nonce"], "tag": vault["tag"]}, self.password)
            try:
                new_enc_vault_key = cryptography.encrypt(
                    dec_vault_key, new_password)
                vault_changes.append({"id": vault["id"], "cipher_text": new_enc_vault_key["cipher_text"],
                                     "salt": new_enc_vault_key["salt"], "nonce": new_enc_vault_key["nonce"], "tag": new_enc_vault_key["tag"]})
            except:
                raise Exception("Error occurred while changing password.")

        try:
            if len(vault_changes) == len(self.vaults):
                db.edit_user_password(self, new_password, vault_changes)
            else:
                raise Exception("Not all vault_keys were correctly updated.")
        except Exception as err:
            print("Error occurred while changing password.", err)

    def add_vault(self, vault_name):
        try:
            db.add_vault(self, vault_name)
        except Exception as err:
            print("Error adding vault.", err)
