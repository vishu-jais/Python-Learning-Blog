import speech_recognition as sr


recognizer = sr.Recognizer()


with sr.Microphone() as source:
    print("Say something...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError:
    print("could not request results. Check your internet connection.")
