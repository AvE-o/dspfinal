import speech_recognition as sr
from gtts import gTTS

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

        try:
            said = r.recognize_google(audio)
            
        except Exception as e:
            print("Exception: " + str(e))

    return said



while True: 
    text = get_audio()
    print(text)