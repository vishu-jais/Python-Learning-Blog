# Program to count vowels and consonants

text = input("Enter a string: ")

# Define vowels
vowels = "aeiouAEIOU"

# Counters
vowel_count = 0
consonant_count = 0

for char in text:
    if char.isalpha():  # Check if the character is a letter
        if char in vowels:
            vowel_count += 1
        else:
            consonant_count += 1

print("Number of vowels:", vowel_count)
print("Number of consonants:", consonant_count)
