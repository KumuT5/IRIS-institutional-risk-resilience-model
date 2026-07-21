from database import login_admin, register_admin

# 🔐 LOGIN
def handle_admin_login(username, password):
    admin = login_admin(username, password)
    return admin  # returns (id, username) or None


# 📝 REGISTER (one-time setup)
def handle_admin_register(username, password):
    success = register_admin(username, password)

    if success:
        return "Admin created"
    else:
        return "Admin exists"
