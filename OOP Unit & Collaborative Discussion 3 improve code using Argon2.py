# Import regular expression for user input verification
import re
import time
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Create a single PasswordHasher instance
ph = PasswordHasher()

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


class AuthenticationSystem:
    def __init__(self):
        self.users = []
        self.failed_attempts = {}  # {username: [timestamps]}

    # Add a new user with secure password handling
    def add_user(self, username, password):
        # 1. Validate username (only letters, numbers, underscores)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return "Invalid username. Only alphanumeric characters and underscores are allowed."

        # 2. Enforce password policy (length, complexity)
        if len(password) < 8:
            return "Weak password. It must be at least 8 characters long."

        # 3. Hash the password with Argon2 (includes salt automatically)
        password_hash = ph.hash(password)

        # 4. Store the hashed password instead of plain text
        self.users.append(User(username, password_hash))

    def authenticate(self, username, password):
        now = time.time()
        # Get previous failed attempts for this username
        attempts = self.failed_attempts.get(username, [])
        # Keep only attempts from last 60 seconds
        attempts = [t for t in attempts if now - t < 60]

        # If 5+ failed logins in last minute → block login attempt
        if len(attempts) >= 5:
            raise Exception("Too many failed attempts. Please try again later.")

        # Loop through stored users to find a match
        for user in self.users:
            if user.username == username:
                try:
                    if ph.verify(user.password_hash, password):
                        # Successful login, reset failed attempts
                        self.failed_attempts[username] = []
                        return "Login successful"
                except VerifyMismatchError:
                    pass

        # Failed login, record the attempt
        attempts.append(now)
        self.failed_attempts[username] = attempts
        return "Invalid username or password"


# Usage
auth_system = AuthenticationSystem()
result1 = auth_system.add_user("adm@#in", "123456red")  # Invalid username
print(result1)
result2 = auth_system.add_user("admin", "12red")  # Weak password
print(result2)
result3 = auth_system.add_user("Payman124", "12red5342efd")
print(result3)

# Simulate an injection attack (note: no SQL here, so it won't bypass)
malicious_input = "admin' OR '1'='1"
print(auth_system.authenticate(malicious_input, "anything"))
