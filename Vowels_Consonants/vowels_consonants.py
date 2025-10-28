# Python program to count vowels and consonants

# Get input from the user
text = input("Enter a string: ")

# Initialize counters
vowels = 0
consonants = 0

# Define vowels
vowel_set = "aeiouAEIOU"

# Loop through each character
for char in text:
    if char.isalpha():  # Check if it's a letters
        if char in vowel_set:
            vowels += 1
        else:
            consonants += 1

# Display the results
print("Number of vowels:", vowels)
print("Number of consonants:", consonants)
