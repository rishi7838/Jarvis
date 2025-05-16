import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text=str(text)
    engin=pyttsx3.init()
    voices = engin.getProperty('voices')  
    engin.setProperty('voice', voices[0].id) 
    engin.setProperty('rate', 174) 
    eel.DisplayMessage(text)
    # print(voices)  not use full
    engin.say(text)
    #when jarvis say and receive text
    eel.receiverText(text)
    engin.runAndWait()

 
# //pip install SpeechRecognition
def takecommand():

    
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('listing........')
        eel.DisplayMessage('listing........')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,10,6)
    try:
        print('recoginzing')
        eel.DisplayMessage('recoginzing....')
        query=r.recognize_google(audio,language='en-in')
        print(f"user said:{query}")
        eel.DisplayMessage(query)
        time.sleep(2)

        # speak(query)  not use full
         
    except Exception as e:
        return ""
    return query.lower()
    
# text=takecommand()

# speak(text)
@eel.expose
def allCommands(message=1):
    if message ==1:
        query = takecommand()
        print("Full command:", query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)


    try:
        

        if "open" in query:
            from engine.feature import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.feature import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.feature import findContact, whatsApp

            contact_no, name = findContact(query)
            if contact_no != 0:
                if "send message" in query:
                    speak("What message should I send?")
                    message_text = takecommand()
                    whatsApp(contact_no, message_text, 'message', name)

                elif "phone call" in query:
                    whatsApp(contact_no, "", 'call', name)

                elif "video call" in query:
                    whatsApp(contact_no, "", 'video call', name)

            else:
                speak("Contact not found.")

        else:
            # print("Command not recognized.")
            # speak("Sorry, I didn't understand.")
            from engine.feature import chatBot
            chatBot(query)
    except Exception as e:
        print("Error occurred:", str(e))
        speak("Something went wrong.")
    eel.ShowHood()
