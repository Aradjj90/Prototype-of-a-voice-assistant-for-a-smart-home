import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import random
import serial
import time, random
import urllib
from urllib.parse import quote
import re, os, sys
import json
import dialogflow
from google.protobuf.json_format import MessageToJson
import pyautogui

mas2 = []
arduino_con = ['arduino is not connected!', 'you forgot to connect the arduino', 'i don\'t see an Arduino. connect it!']
global command_flag

engine = pyttsx3.init()
voices = engine.getProperty('voices')

count = 1  # terms in the note
flag_internet = True  # Internet availability flag
flag_language = True  # flag which language to speak


def speak(audio):
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 135)  # setting up new voice rate
    engine.say(audio)
    engine.runAndWait()


def read(audio):
    engine.setProperty('voice', voices[2].id)
    engine.setProperty('rate', 135)  # setting up new voice rate
    engine.say(audio)
    engine.runAndWait()


def start_greeting():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I'm a voice assistant - Jessica! Please tell me what you wish")


def takeCommand():
    global flag_internet
    global command_flag
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listning...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        if flag_language:
            query = r.recognize_google(audio).lower()
            if not flag_internet:
                speak("connected to the internet")
            print(f"You said : {query}\n")
            flag_internet = True
        else:
            query = r.recognize_google(audio, language="uk-UA").lower()
    except sr.UnknownValueError:
        if not flag_internet:
            speak("connected to the internet")
        print("sorry, i don't understand you")
        flag_internet = True
        command_flag = True
        return 'None'
    except sr.RequestError:
        if flag_internet:
            speak("no internet!")
        flag_internet = False
        return 'None'
    return query


def chatbot_message(s):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "small-talk-fxya-123456789.json"
    project_id = "!@#$%^&*" # your project id on dialogflow
    session_id = "123456789" # your session id on dialogflow
    language_code = "en"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    phrase = s
    text_input = dialogflow.types.TextInput(text=phrase, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response_dialogflow = session_client.detect_intent(session=session, query_input=query_input)
    response = MessageToJson(response_dialogflow.query_result)

    responseJson = json.loads(response)
    response_message = responseJson['fulfillmentText']
    if response_message:
        return response_message
    else:
        return 'I don\'t anderstend'


def find_youtube(x):
    mas = []
    sq = 'http://www.youtube.com/results?search_query=' + quote(x) + '&sp=CAE%253D'
    doc = urllib.request.urlopen(sq).read().decode('cp1251', errors='ignore')
    match = re.findall("\?v\=(.+?)\"", doc)
    if not (match is None):
        for ii in match:
            if len(ii) < 25:
                mas.append(ii)
    mas = dict(zip(mas, mas)).values()

    for y in mas: mas2.append('https://www.youtube.com/watch?v=' + y)
    return mas2


try:
    anrduinoData = serial.Serial('com3', 9600)
except serial.serialutil.SerialException:
    speak('arduino is not connected')


def arduino_control(query):
    global command_flag
    # ----------------------------------------------------------------------------------------------------------------------
    # TV control
    if 'turn on tv' in query or 'turn off tv' in query:
        try:
            command_flag = True
            anrduinoData.write(b'1')
            speak('turn')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'tv menu' in query:
        try:
            command_flag = True
            anrduinoData.write(b'2')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'go up' in query:
        try:
            command_flag = True
            anrduinoData.write(b'3')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'go down' in query:
        try:
            command_flag = True
            anrduinoData.write(b'4')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'select' in query:
        try:
            command_flag = True
            anrduinoData.write(b'5')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'turn on discovery science' in query:
        try:
            command_flag = True
            anrduinoData.write(b'6')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif '5 position app' in query or '5 position up' in query:
        try:
            command_flag = True
            anrduinoData.write(b'7')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif '5 position down' in query:
        try:
            command_flag = True
            anrduinoData.write(b'8')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    # ----------------------------------------------------------------------------------------------------------------------
    # rolls control
    elif 'rolls down' in query or 'close window' in query:
        try:
            command_flag = True
            anrduinoData.write(b'9')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'rolls up' in query or 'open window' in query:
        try:
            command_flag = True
            anrduinoData.write(b'A')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
            # Lower the right roll
    elif 'close right part of the window' in query:
        try:
            command_flag = True
            anrduinoData.write(b'B')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
            # Raise the right roll
    elif 'open right part of the window' in query:
        try:
            command_flag = True
            anrduinoData.write(b'C')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))

    elif 'close left part of the window' in query:
        try:
            command_flag = True
            anrduinoData.write(b'D')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
            # Raise the right roll
    elif 'open left part of the window' in query:
        try:
            anrduinoData.write(b'E')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))

    # -----------------------------------------------------------------------------------------------------------------------
    # Table lamp control
    elif 'turn on table lamp' in query or 'turn on the table light' in query:
        try:
            command_flag = True
            anrduinoData.write(b'F')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    elif 'turn off table lamp' in query or 'turn off the table light' in query:
        try:
            command_flag = True
            anrduinoData.write(b'G')
        except serial.serialutil.SerialException:
            speak('not opened arduino port')
        except NameError:
            speak(random.choice(arduino_con))
    return 'None'


if __name__ == "__main__":
    start_greeting()
    command_flag = True
    while True:
        t0 = time.time()
        query = takeCommand()
        Arduino_control(query)
        if ('jess' in query or 'jc' in query or 'yes' in query or 'just' in query) and ('what time' in query):
            command_flag = True
            #speak Ukrainian
            if 'in ukrainian' in query:
                flag_language = False
                now = datetime.datetime.now()
                read(("зараз " + str(now.hour) + ":" + str(now.minute)))
                flag_language = True
                #speak English
            else:
                now = datetime.datetime.now()
                speak("now is " + str(now.hour) + ":" + str(now.minute))
        # Open the file
        elif ('open' in query) and ('conflict' in query):
            os.startfile('D:\\StarConflikt\\StarConflict\\launcher.exe')
            command_flag = True
        elif ('close' in query) and ('conflict' in query):
            os.system('TASKKILL /F /IM launcher.exe')
            command_flag = True
        elif 'open arduino port' in query:
            try:
                command_flag = True
                anrduinoData.open()
            except serial.serialutil.SerialException:
                speak('arduino is not connected')
        elif 'close arduino port' in query:
            anrduinoData.close()
            command_flag = True
            speak('arduino port is disabled')

        # ______________________________________________________________________________________________________________________
        elif 'open hit fm' in query or 'open hear fm' in query:
            webbrowser.open('http://online.hitfm.ua/HitFM_HD')
            command_flag = True
            speak('opened')
        elif 'open google' in query:
            webbrowser.open('https://www.google.com.ua')
            command_flag = True
            speak('opened')
        elif ('search' in query or 'find' in query) and 'google' in query:
            command_flag = True
            query = query.replace('search', '')
            query = query.replace('find', '')
            query = query.replace('in google', '')
            query = query.strip()
            webbrowser.open('https://www.google.at/search?client=opera&hs=d5G&ei=kt4xXqDpCoTZwQK77JegDw&q=' + query)
            speak('opened')
        elif 'open youtube' in query:
            webbrowser.open_new('https://www.youtube.com')
            command_flag = True
            speak('opened')
        # ______________________________________________________________________________________________________________________
        # opening a YouTube video thread
        elif ('search' in query or 'find' in query) and 'youtube' in query:
            command_flag = True
            query = query.replace('search', '')
            query = query.replace('find', '')
            query = query.replace('in youtube', '')
            query = query.strip()
            webbrowser.open('http://www.youtube.com/results?search_query=' + query + '&sp=CAE%253D')

            speak('opened')
            find_youtube(query)
            speak('I found' + str(len(mas2)) + 'forces')
            if len(mas2) >= 10:
                speak('i can open the first 10')
            speak('which you want to open?')
            while True:
                query = takeCommand()
                print(query)
                if 'first video' in query:
                    webbrowser.open(mas2[0])
                    break
                elif 'second video' in query:
                    webbrowser.open(mas2[1])
                    break
                elif 'third video' in query or 'start video' in query:
                    webbrowser.open(mas2[2])
                    break
                elif 'force video' in query or 'horse video' in query:
                    webbrowser.open(mas2[3])
                    break
                elif 'fives video' in query or '5 video' in query:
                    webbrowser.open(mas2[4])
                    break
                elif 'six video' in query or 's********' in query:
                    webbrowser.open(mas2[5])
                    break
                elif '7th video' in query or '7 video' in query:
                    webbrowser.open(mas2[6])
                    break
                elif 'aids video' in query or '8 video' in query:
                    webbrowser.open(mas2[7])
                    break
                elif 'nines video' in query or '9 video' in query:
                    webbrowser.open(mas2[8])
                    break
                elif 'dance video' in query or '10 video' in query:
                    webbrowser.open(mas2[9])
                    break
                elif 'nothing interesting' in query or 'no' in query:
                    break

        elif 'play some music' in query:
            music_dir = "D:\\Music"
            songs = os.listdir(music_dir)
            random_gen = random.randint(0, len(songs) - 1)
            os.startfile(os.path.join(music_dir, songs[random_gen]))
            command_flag = True
        # Connecting a sound card

        elif 'additional sound card' in query:
            pyautogui.hotkey('ctrl', 'o')
            speak('Where you hear me?')
            command_flag = True

        elif 'default sound card' in query:
            pyautogui.hotkey('ctrl', 'q')
            speak('Where you hear me?')
            command_flag = True
        # ------------------------------------
        elif 'close music player' in query:
            os.system('TASKKILL /F /IM PotPlayerMini.exe')
            command_flag = True
        elif 'write note' in query:
            command_flag = True
            inFile = open('note.txt', 'w')
            inFile.close()
            with open('note.txt', 'a') as inFile:
                speak("I'm ready to write")
                flag_language = False
                while True:
                    query = takeCommand()
                    print(query)
                    text = query
                    if "None" in text:
                        speak("sorry, i don't understand you")
                        continue
                    if 'stop' in query or 'enough' in query or 'буде' in query or 'достатньо' in query or 'кінець' in query:
                        count = 1
                        flag_language = True
                        speak("i finished recording")
                        break
                    inFile.write(str(count) + " - " + text + ", - ")
                    count = count + 1
                    speak("ok")
                speak("do you want to read the writing")
                query = takeCommand()
            if 'yes' in query:
                with open('note.txt') as inFile:
                    read(inFile.read())
            else:
                pass

        elif ('jess' in query or 'yes' in query or 'just' in query) and (
                'off' in query or 'exit' in query or 'of' in query):
            speak("i am off, bye")
            command_flag = True
            sys.exit()
        if command_flag == False:
            speak(chatbot_message(query))
        print(time.time() - t0)
        command_flag = False
