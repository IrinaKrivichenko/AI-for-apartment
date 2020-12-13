# https://www.youtube.com/watch?v=kyZ_5cvrXJI&t=216s


"""
speaker = pyttsx3.init()
for num in range(7, pages):
    page = pdfReader.getPage(num)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()
"""
# Чтение вслух
import os
import re
import vlc
import playsound
import datetime
import time
from gtts import gTTS
import PyPDF2

# Для того чтобы не возникало коллизий при удалении mp3 файлов
# заведем переменную mp3_nameold в которой будем хранить имя предыдущего mp3 файла
mp3_nameold = '111'
mp3_name = "1.mp3"

# Инициализируем звуковое устройство

#pygame.init()
#pygame.mixer.init()

# Открываем файл с текстом и по очереди читаем с него строки в ss
book = open('Data_Science_for_Business_What_you_need_to_know_about_data_mining.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
pages = 40#pdfReader.numPages

for num in range(39, pages):
    page = pdfReader.getPage(num)
    text = page.extractText()
    # Делим прочитанные строки на отдельные предложения
    #split_regex = re.compile(r'[.|!|?|…]')
    #sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(text)])
    sentences = text

    # Перебираем массив с предложениями

    # Эта строка отправляет предложение которое нужно озвучить гуглу
    tts = gTTS(text=text, lang='en')
    # Получаем от гугла озвученное предложение в виде mp3 файла
    tts.save(mp3_name)
    # Проигрываем полученный mp3 файл
    playsound.playsound(mp3_name)
    #while playsound:

    #sound_file = vlc.MediaPlayer(mp3_name)       #vlc
    #my_song = pygame.mixer.sound(os.path.join(IMG_FOLDER, mp3_name))  #mixer
    #sound_file.play()       #vlc
    #my_song.play()         #mixer
    #pygame.mixer.music.load(mp3_name)      #mixer
    #pygame.mixer.music.play()          #mixer
    #while pygame.mixer.music.get_busy():   #mixer
    #size = sound_file.__sizeof__()/16+.2       #vlc
    #time.sleep(size)       #vlc
    # Если предыдущий mp3 файл существует удаляем его
    # чтобы не захламлять папку с приложением кучей mp3 файлов
    if (os.path.exists(mp3_nameold) and (mp3_nameold != "1.mp3")):
        os.remove(mp3_nameold)
    mp3_nameold = mp3_name
    # Формируем имя mp3 файла куда будет сохраняться озвученный текст текущего предложения
    # В качестве имени файла используем текущие дату и время
    now_time = datetime.datetime.now()
    mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    # Читаем следующую порцию текста из файла
    #ss = f.readline()

# Закрываем файл
#f.close

# Устанвливаем текущим файлом 1.mp3 и закрываем звуковое устройство
# Это нужно чтобы мы могли удалить предыдущий mp3 файл без колизий
#mixer.music.load('1.mp3')
#mixer.stop
sound_file.stop()
#mixer.quit

# Удаляем последний предыдущий mp3 файл
if (os.path.exists(mp3_nameold)):
    os.remove(mp3_nameold)