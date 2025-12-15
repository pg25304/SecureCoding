from calendar import error


class Validator:
    #class state (shared across all instances)
    rules_enabled = True

    def __init__(self):
        #object state (unique per instance)
        self.errors = []

    #1.Instance method ->depends on object state
    def add_error(self, message):
        self.errors.append(message)
        return f"Error added: {message}"

    #2.class method-> depends onclass state
    @classmethod
    def toggle_rules(cls, enabled: bool):
        cls.rules_enabled = enabled
        return f"Rules enabled set to {cls.rules_enabled}"

    #3.static method -> independent of object/class state
    @staticmethod
    def is_email_valid(email: str):
        return "@" in email and "." in email

#Example usage
if __name__ == "__main__":

    #Instance method usage
    v = Validator()
    print(v.add_error("Invalid password")) # Output: Error added: Invalid password

    #Class method usage
    print(Validator.toggle_rules(False)) # Output: Rules enabled set to False

    #static method usage
    print(Validator.is_email_valid("banana")) # -> False

    #⚖️ What’s Happening
# Instance method (add_error) → works with self.errors, unique to each object.
# Class method (toggle_rules) → changes rules_enabled, shared across all Validator objects.
# Static method (is_email_valid) → just checks the string; doesn’t care about any object or class state.#
#This pattern is common in real-world code:
# Instance methods track per-user or per-object data.
# Class methods manage global settings or alternative constructors.
#  Static methods provide utility checks or calculations.
