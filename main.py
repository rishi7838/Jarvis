import os 
import eel

from engine.feature import *
from engine.command import *
from engine.auth import recoganize

def start():
    
    eel.init("www")


    playAssistantSound()
    @eel.expose
    def init():
        subprocess.call([r'device.bat']) 
        eel.hideLoader()
        speak("Ready for face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak(" face Authentication sucessfully")
            eel.hideFaceAuthSuccess()
            speak("Welcome! Rishi sir")
            #Hide Start Page and display blob
            eel.hideStart()
            playAssistantSound()
        else:
            speak("face Authentication fail")


    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html',mode=None,host='localhost' ,block=True)

    