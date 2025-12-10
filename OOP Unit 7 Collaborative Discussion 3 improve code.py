#import regular expression for user input verification
import re
from ctypes import HRESULT

import bcrypt
import time

class User:
    def __init__(self, username, password_hash):
         self.username = username
         self.password_hash = password_hash


class AuthenticationSystem:
    def __init__(self):
        self.users = []
        self.failed_attempts = {} #{username: [timestamps]}
    #Add a new user with secure password handling
    def add_user(self, username, password):
        # 1. Validate username (only letters, numbers, underscores)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return "Invalid username. Only alphanumeric characters and underscores are allowed."
        #2. Enforce password policy (length, complexity)
        if len(password)<8:
            return "Weak password. It must be at least 8 characters long."
        #3from hash the password with bcrypt (includes salt automatically)
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        #4. Store the hashed password instead of plain text
        self.users.append(User(username, password_hash))


    def authenticate(self, username, password):
        now = time.time()
        #Get previous failed attempts for this username
        attempts = self.failed_attempts.get(username, [])#if there are not return empty list
        #keep only attempts from last 60 seconds
        attempts = [time for t in attempts if now -t < 60]
        #If 5+ failed logins in last minute → block login attempt
        if len(attempts) >= 5:
            raise Exception("Too many failed attempts. Please try again later.")
        #Loop through stored users to find a match
        for user in self.users:
            if user.username == username and bcrypt.checkpw(password.encode(), username.password_hash):
                #Successful login, reset failed attempts
                self.failed_attempts[username] = []
                return "Login successful"
        #Failed login, record the attempt
        attempts.append(now)
        self.failed_attempts[username] = attempts
        return "Invalid username or password"




# Usage
auth_system = AuthenticationSystem()
result1 = auth_system.add_user("adm@#in", "123456red") # Invalid username
print(result1)
result2 = auth_system.add_user("admin", "12red") # weak password
print(result2)
# Simulate an injection attack
malicious_input = "admin' OR '1'='1"

print(auth_system.authenticate(malicious_input, "anything"))
# Output: True (Vulnerable to SQL injection)

#password.encode('utf-8'): This converts the password string into bytes using UTF-8 encoding. Bcrypt requires
# a bytes-like object as input.
#bcrypt.gensalt(): This generates a random salt value. A salt is a random string added to the password before
# hashing to prevent attacks like rainbow table attacks.
#bcrypt.hashpw(...): This function hashes the password (converted to bytes) using the generated salt.
# The hashed password is then returned as a bytes object.
#So, hashed_password will hold the securely hashed version of the input password, which can be stored
# in a database for secure password storage.
#- Validation: Rejects usernames with dangerous characters and enforces password rules.
#Hashing: bcrypt.gensalt() generates a random salt, and bcrypt.hashpw() stores a salted hash.
# Authentication: Compares entered password against the stored hash using bcrypt.checkpw().
#for user in self.users: This line starts a loop that iterates over each user object in the self.users collection.
#if user.username == username and bcrypt.checkpw(password.encode(), username.password_hash):
# This checks two conditions:
#If the current user's username matches the provided username.
#If the provided password matches the hashed password stored for the user using bcrypt.
#If both conditions are true, the code inside the if statement executes:
#self.failed_attempts[username] = []: Resets the list of failed login attempts for the user.
#return True: Indicates a successful login and stops the function execution.
