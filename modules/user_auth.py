from database import register_user, login_user, update_usage
import hashlib


# -------------------------------
# PASSWORD HASHING
# -------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------
# USER REGISTRATION HANDLER
# -------------------------------
def handle_user_register(company_name,username, email, password):

    # Basic validation
    if not company_name or not email or not password:
        return "All fields are required"

    if len(password) < 6:
        return "Password must be at least 6 characters"

    # Hash password before sending to DB
    hashed_password = hash_password(password)

    # Call DB layer
    result = register_user(company_name,username, email, hashed_password)

    return result


# -------------------------------
# USER LOGIN HANDLER
# -------------------------------
def handle_user_login(username, password):

    if not username  or not password:
        return None, "Enter username  and password"

    # Hash input password
    hashed_password = hash_password(password)

    user = login_user(username, hashed_password)
    

    if not user:
        return None, "User not found"

    if user["password"] != hashed_password:
        return None, "Incorrect password"

    update_usage(user["id"])

    return user, "success"
    
    
