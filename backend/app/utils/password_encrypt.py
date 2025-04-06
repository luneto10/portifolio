from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Hash a password using Argon2.
    :param password: The plaintext password to hash.
    :return: The hashed password.
    """
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password using Argon2.
    :param password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    try:
        ph.verify(hashed_password, password)
        return True
    except exceptions.VerifyMismatchError:
        return False