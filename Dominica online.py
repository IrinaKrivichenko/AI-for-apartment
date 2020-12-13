# Alexa https://www.youtube.com/watch?v=AWvsXxDtEkU&t=118s


import speech_recognition as sr
import playsound
import datetime
import time
from gtts import gTTS
import os
#import pywhatkit
#import wikipedia
#import pyjokes

cmds = {
    "play ..." : ('включи', 'воспроизведи' ),
    "wikipedia ..." : ('кто такой', 'что такое', 'посмотри в википедии', 'глянь в википедии' ),
    "time": ('текущее время', 'сейчас времени', 'который час', 'сколько время' ),
    "date": ('какое сегодня число', 'какой сегодня день', 'какой сегодня день')
}


listener = sr.Recognizer()
mp3_nameold = 'mp3old'
mp3_name = "mp3.mp3"
speaking_person = ""

def recognize_command(cmd):
    for c, v in cmds.items():
        for x in v:
            if cmd.find(x) != -1 :
                print(c)
                if c.find("...") != -1:
                    c = c.replace('...', cmd.replace(x, ''))
                return c
    return cmd

def talk(text):
    global mp3_name, mp3_nameold
    tts = gTTS(text=text, lang='ru')
    tts.save(mp3_name)
    playsound.playsound(mp3_name)
    if (os.path.exists(mp3_nameold) and (mp3_nameold != "1.mp3")):
        os.remove(mp3_nameold)
    mp3_nameold = mp3_name

def exec_command(command):
     if 'play' in command:
         song = command.replace('play', '')
         talk('включаю ' + song)
         #pywhatkit.playonyt(song)
     elif 'time' in command:
         time = datetime.datetime.now().strftime('%I:%M')
         talk('Сейчас ' + time)
     elif 'date' in command:
         date = datetime.datetime.now().strftime('%d/%m/%Y')
         days_of_week = ["понедельник ", "вторник ", "среда ", "четверг ", "пятница ", "суббота ", "воскресенье "]
         day_of_week = days_of_week[datetime.datetime.now().weekday()]
         talk('Сегодня ' + day_of_week + date)
     elif 'wikipedia' in command:
         what = command.replace('wikipedia', '')
         info = wikipedia.summary(what, 1)
         print(info)
         talk(info)
     elif 'are you single' in command:
         talk('I am in a relationship with wifi')
     elif 'joke' in command:
         talk(pyjokes.get_joke())
     else:
         talk('Команда не понятна')


def take_command():
    try:
        with sr.Microphone() as source:
            print('Слушаю...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language="ru-RU")
            command = command.lower()
            print(command)
            if 'доминика' in command:
                command = command.replace('доминика', '')
                command = recognize_command(command)
                exec_command(command)
    except Exception as e:
        print(e)



def run_alexa():
    take_command()


while True:
    run_alexa()