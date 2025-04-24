import pyttsx3
import speech_recognition as sr
 
def speak(text):
    engin=pyttsx3.init()
    voices = engin.getProperty('voices')  
    engin.setProperty('voice', voices[1].id) 
    engin.setProperty('rate', 174) 
    print(voices)
    engin.say(text)
    engin.runAndWait()


# //pip install SpeechRecognition
def takecommand():

    
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('listing........')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,10,6)
    try:
        print('recoginzing')
        query=r.recognize_google(audio,language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        return ""
    return query.lower()
    
text=takecommand()

speak(text)