# CountVowelsConsonants.py
# Contribution to VGLUG Python-Learning-Blog
# Problem: Count vowels and consonants in a given string
# Author: Priyadharshni G


def count_vowels_consonants(text):
    """
    Count vowels and consonants in the given string.
    Only alphabetic characters are considered.
    Returns a tuple (vowel_count, consonant_count).
    """
    vowels = "aeiou"  # Define all vowels (lower and upper case)
    v_count = 0            # Initialize vowel count
    c_count = 0            # Initialize consonant count
    text=text.lower()
    for char in text:
        if char.isalpha():      # Check if character is a letter
            if char in vowels:
                v_count += 1    # Increment vowel count
            else:
                c_count += 1    # Increment consonant count

    return v_count, c_count

def main():
    # Prompt user for input
    text = input("Enter a string: ")
    vowels, consonants = count_vowels_consonants(text)
    
    print(f"Vowels: {vowels}")
    print(f"Consonants: {consonants}")

if __name__ == "__main__":
    main()
