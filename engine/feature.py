from shlex import quote
import struct
import subprocess
import time
from hugchat import hugchat
from playsound import playsound 

import eel
import pvporcupine
import pyaudio
import pyautogui

 
import os

import pywhatkit as kit
import re
import webbrowser
import sqlite3
from engine.config import ASSISTANT_NAME
from engine.command import speak
 
from engine.helper import extract_yt_term, remove_words


con= sqlite3.connect("jarvis.db")
cursor = con.cursor()


#playing assistant file
@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)



def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term + " Rishi Sir jii")
    kit.playonyt(search_term)



def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


 #find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME,'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video','']

    query= remove_words(query, words_to_remove)
    try:
        query=query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    


def whatsApp(mobile_no, message, flag, name):
    import pygetwindow as gw

    if flag == 'message':
        target_tab = 12
        jarvis_message = f"Message sent successfully to {name}"
    elif flag == 'call':
        target_tab = 6
        message = ''
        jarvis_message = f"Calling {name}"
    else:
        target_tab = 5
        message = ''
        jarvis_message = f"Starting video call with {name}"

#encode the msg for url
    encoded_message = quote(message)
    print(f"Encoded message: {encoded_message}")
    #constrtuct url
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    # Launch WhatsApp
    subprocess.run(full_command, shell=True)
    time.sleep(6)  # Wait for WhatsApp to open

    # Bring WhatsApp window to front (optional, works with pygetwindow and pywin32)
    try:
        window = gw.getWindowsWithTitle("WhatsApp")[0]
        window.activate()
        time.sleep(1)
    except Exception as e:
        print("Could not focus WhatsApp window:", e)

    # Reset focus using ctrl + f
    # Ensure chat is actually opened
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.typewrite(name, interval=0.05)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1.5)  # Let chat load

    # Use tab to reach message input box
    for i in range(target_tab):
        pyautogui.press('tab')
        time.sleep(0.1)

    pyautogui.press('enter')
    speak(jarvis_message)


#chat bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
