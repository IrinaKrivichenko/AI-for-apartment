# https://www.youtube.com/watch?v=YeS755SPSI8

# Голосовой ассистент КЕША 1.0 BETA
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

# настройки
opts = {
    "alias": ('кеша', 'кеш', 'инокентий', 'иннокентий', 'кишун', 'киш',
              'кишаня', 'кяш', 'кяша', 'кэш', 'кэша'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "hi": ('привет', 'здравствуй', 'приветствую')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            print(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("D:\\Jarvis\\res\\radio_record.m3u")

    elif cmd == 'hi':
        # рассказать анекдот
        speak("привет")

    else:
        print('Команда не распознана, повторите!')


# запуск
r = sr.Recognizer()
m = sr.Microphone()#device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices') # Получить список голосов
# Перебрать установленные голоса и вывести имя каждого
for voice in voices:
    print(voice.name)

#voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', 'russian')



# forced cmd test


speak("hi, my name is kesha")
speak("Кеша слушает")
#stop_listening = r.listen_in_background(m, callback)
#while True: time.sleep(0.1) # infinity loop