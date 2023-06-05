
from Crypto.Cipher import AES

"""
Encrypts data using AES encryption.

Keyword arguments:
key -- The key to use for encryption.
data -- The data to encrypt.

Return:
The encrypted data.
"""


def aes_encryption(key_str: str, data_str: str):

    # Convert the key and data to bytes
    key = key_str.encode('utf-8')
    data = data_str.encode('utf-8')

    # Create the cipher
    cipher = AES.new(key, AES.MODE_EAX)

    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return ciphertext
