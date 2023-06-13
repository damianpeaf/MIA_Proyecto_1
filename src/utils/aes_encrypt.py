
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

"""
Encrypts data using AES encryption.

Keyword arguments:
key -- The 16 bytes key str to use for encryption.
data -- The data to encrypt.

Return:
The encrypted data.
"""


def aes_encryption(key_str: str, data_str: str) -> str:

    # Convert the key and data to bytes
    key = key_str.encode('utf-8')
    data = data_str.encode('utf-8')

    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext.hex()
