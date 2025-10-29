# A Python program to demonstrate default and keyword arguments in functions.

def greet(name="User", message="Welcome!"):
    print(f"Hello {name}, {message}")

# Calling the function in different ways
greet()                          # Uses both default values
greet("Anu")                     # Overrides only name
greet(message="Good Morning!")   # Overrides only message
greet("Riya", "Have a nice day!") # Overrides both
