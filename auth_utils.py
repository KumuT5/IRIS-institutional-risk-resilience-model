import re
import bcrypt
import random

# -------------------------------
# USERNAME VALIDATION
# -------------------------------
def is_valid_username(username):
    username = username.strip()
    return re.match(r'^[A-Za-z0-9_]+$', username) is not None


# -------------------------------
# COMPANY NAME VALIDATION
# -------------------------------
def is_valid_company(company_name):
    company_name = company_name.strip()
    return re.match(r'^[A-Za-z0-9 ]+$', company_name) is not None


#--------------------------------
#  PASSWORD VALIDATION
#--------------------------------
def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode(), stored_hash)

def generate_otp():
    return str(random.randint(100000, 999999))
