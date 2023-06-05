from utils import aes_encryption

USERS_FILE = 'users.txt'
AES_KEY = 'miaproyecto12345'

"""
Takes the username and password and validates them against the users.txt file.

Keyword arguments:
username -- The username to validate.
password -- The password to validate.

Returns:
True if the username and password are valid, False otherwise.
"""


def validate_user(username: str = '', password: str = '') -> bool:

    with open(USERS_FILE, 'r') as users_file:
        lines = users_file.readlines()

        username_found = False

        for line in lines:

            # Skip empty lines
            if line.trim() == '':
                continue

            # If the username was found, check the password
            if username_found:

                # TODO: Check if the aes encryption its encrypting the password correctly
                if line.trim() == aes_encryption(AES_KEY, password).hex():
                    return True

                # If the password was not found, return False
                return False

            if line.trim() == username.trim():
                username_found = True

    return False
