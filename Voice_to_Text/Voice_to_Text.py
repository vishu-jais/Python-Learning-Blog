# Importing necessary libraries
import speech_recognition as sr  # Library for speech recognition (voice to text)
import pyttsx3                   # Library for text-to-speech conversion
from datetime import datetime    # For adding timestamps when saving files

def speak(text):
    """Function to make the system speak text."""
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Convert the text into speech
    engine.say(text)
    # Play the speech
    engine.runAndWait()

def record_voice():
    """Record audio from microphone and convert to text."""
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    # Use the default microphone as the audio source
    mic = sr.Microphone()

    # Listen to the user's voice input 
    with mic as source:
        print("Adjusting for background noise... Please wait...")
        # Adjust the recognizer to ignore background noise
        recognizer.adjust_for_ambient_noise(source)
        print("🎙 Speak now...")
        # Capture the audio from the microphone
        audio = recognizer.listen(source)

    try:
        print("Transcribing your speech...")
        # Use Google Speech Recognition to convert audio to text
        text = recognizer.recognize_google(audio)
        print("✅ You said:", text)
        return text

    # If speech was not recognized properly
    except sr.UnknownValueError:
        print("Sorry, I couldn’t understand your speech.")
        speak("Sorry, I couldn’t understand your speech.")
        return None

    # If there was an issue with the Google API or internet
    except sr.RequestError:
        print("Network error. Check your internet connection.")
        speak("Network error. Please check your internet connection.")
        return None


def save_to_file(text):
    """Save the recognized text to a file with timestamp."""
    # Only save if text was successfully recognized
    if text:
        # Generate a unique filename with current date and time
        filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
         # Open the file in write mode and save the text
        with open(filename, "w") as file:
            file.write(text)
        print(f"📁 Transcription saved as: {filename}")
        # Confirm the save with voice feedback
        speak("Your speech has been saved successfully.")
    else:
        print("⚠ No text to save.")

def main():
    print("==== VOICE TO TEXT TRANSCRIPTION ====")
     # Greet the user with a spoken message
    speak("Welcome to Voice to Text Transcription Project")
    
    # Record voice input and get the converted text
    text = record_voice()
    # Record voice input and get the converted text
    save_to_file(text)

    print("🎉 Task completed!")

# This ensures the program runs only when executed directly
if __name__ == "__main__":
    main()
