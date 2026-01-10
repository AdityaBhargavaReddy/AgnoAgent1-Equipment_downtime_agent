
import speech_recognition as sr
# ---------------- TEXT ----------------
def get_text_input():
    return input("Enter text: ")


# ---------------- VOICE ----------------
def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return "Voice not recognized"


# ---------------- IMAGE  ----------------
def get_image_input():
    return "Generate text from this image: https://www.treadmillreviews.net/wp-content/uploads/2012/04/broken-treadmill-display.png.webp"