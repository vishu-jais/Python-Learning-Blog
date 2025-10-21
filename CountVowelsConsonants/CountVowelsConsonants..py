# CountVowelsConsonants.py
# Contribution to VGLUG Python-Learning-Blog
# Problem: Count vowels and consonants in a given string

def count_vowels_consonants(text):
    """
    Count vowels and consonants in the given string.
    Only alphabetic characters are considered.
    Returns a tuple (vowel_count, consonant_count).
    """
    vowels = "aeiou"  
    v_count = 0            
    c_count = 0            
    text=text.lower()
    for char in text:
        if char.isalpha():      
            if char in vowels:
                v_count += 1    
            else:
                c_count += 1    

    return v_count, c_count

def main():
    text = input("Enter a string: ")
    vowels, consonants = count_vowels_consonants(text)
    
    print(f"Vowels: {vowels}")
    print(f"Consonants: {consonants}")

if __name__ == "__main__":
    main()
