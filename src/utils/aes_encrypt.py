
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_encryption(key_str: str, data_str: str) -> str:

    # Convert the key and data to bytes
    key = key_str.encode('utf-8')
    data = data_str.encode('utf-8')

    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext.hex()


def aes_decryption(key_str: str, data_str: str) -> str:

    # Convert the key and data to bytes
    key = key_str.encode('utf-8')
    data = bytes.fromhex(data_str)

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(data)
    return unpad(plaintext, AES.block_size).decode('utf-8')
