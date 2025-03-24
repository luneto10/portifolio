from passlib.context import CryptContext

hash_helper = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    """
    Hash a password.
    :param password: The plaintext password to hash.
    :return: The hashed password.
    """
    return hash_helper.hash(password)

def verify_password(password: str, hashed_password: str):
    """
    Verify a password against a hashed password.
    :param password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return hash_helper.verify(password, hashed_password)