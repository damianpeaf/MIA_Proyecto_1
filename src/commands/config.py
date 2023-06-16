from enum import Enum


class Store:
    IS_LOGGED: bool = False


class CommandEnvironment(Enum):
    LOCAL = 1
    CLOUD = 2


class CommandConfig:

    def __init__(self, environment: CommandEnvironment, log_encryption: bool, read_encryption: bool, encryption_key: str):
        self.environment = environment
        self.log_encryption = log_encryption  # ? Redundant
        self.read_encryption = read_encryption  # ? IDK if this is needed
        self.encryption_key = encryption_key

    def __str__(self) -> str:

        return f"""
        Environment: {self.environment}
        Log encryption: {self.log_encryption}
        Read encryption: {self.read_encryption}
        Encryption key: {self.encryption_key}
        """
