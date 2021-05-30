""" helper functions of bankofirvine 
"""
import re
import os
import hashlib
import uuid
import secrets

comments = {
            "Fred" : "Great service! I'm banking here forever.",
            "Barney" : "Wilma was super helpful in setting up my account.",
            "Betty" : "Had to a wait a bit, but wonderful service when they got to me."
        }

# Numeric validation (e.g. balance)
def validate_num (num_input):
    return re.match("^([1-9][0-9]*|0)(\.[0-9]{2})$", num_input) != None

# String validation (e.g. account name, password)
def validate_str (str_input):
    return re.match("(^[_\\-\\.0-9a-z]{1,127}$)", str_input) != None

def create_salt():
    return os.urandom(32)

def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

def create_random_userid():
    return str(uuid.uuid4())    

def gen_key():
    return secrets.token_urlsafe(16)

# String validation for comments.
def validate_comments(str_input):
    return re.match("(^[A-Za-z,\\s]+[.]$)", str_input) != None
