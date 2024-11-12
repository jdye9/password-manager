import base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from argon2 import PasswordHasher

ph = PasswordHasher()


class Cryptography:

    def encrypt(plain_text, key):
        # use Argon2 to get a private key from the password (base64 encoded output)
        hash = ph.hash(key)

        # format to 32 bytes for AES key
        private_key = base64.b64decode(hash.split("$")[5] + "=")
        salt = base64.b64decode(hash.split("$")[4] + "==")

        # create cipher config
        cipher_config = AES.new(private_key, AES.MODE_GCM)

        # return a dictionary with the encrypted text
        cipher_text, tag = cipher_config.encrypt_and_digest(
            bytes(plain_text, 'utf-8'))

        return {
            'cipher_text': base64.b64encode(cipher_text).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8'),
            'nonce': base64.b64encode(cipher_config.nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8')
        }

    def decrypt(enc_dict, key):
        # decode the dictionary entries from base64
        cipher_text = base64.b64decode(enc_dict['cipher_text'])
        salt = base64.b64decode(enc_dict['salt'])
        nonce = base64.b64decode(enc_dict['nonce'])
        tag = base64.b64decode(enc_dict['tag'])

        # use Argon2 to get a private key from the password and previously saved salt
        hash = ph.hash(key, salt=salt)

        # format to 32 bytes for AES key
        private_key = base64.b64decode(hash.split("$")[5] + "=")

        # create the cipher config
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        # decrypt the cipher text
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)

        return decrypted.decode('utf8')

    def generate_vault_key():
        return base64.b64encode(get_random_bytes(32)).decode('utf-8')
