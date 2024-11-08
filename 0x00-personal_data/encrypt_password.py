#!/usr/bin/env python3
import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a salted hash.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        bytes: The hashed password as a byte string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if the provided plain-text password matches the hashed password.
    
    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain-text password to check.
        
    Returns:
        bool: True if the password is valid (matches the hash), False otherwise.
    """
    # Compare the plain-text password with the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
