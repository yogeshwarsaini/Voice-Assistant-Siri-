import pyttsx3
import speech_recognition as sr
import webbrowser
import smtplib
import requests
import datetime
import json
import os
import random
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"Speaking: {audio}")  # Debugging line
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Kripya phir se kahiye...")
        return "None"
    return query.lower()

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('yogismash123@gmail.com', 'Yogismash123@')
        server.sendmail('yogismash123@gmail.com', to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email")

def getWeather(city):
    api_key = "2ef845d3537d97030f55e30fc23b916a"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    
    # Debugging output
    print(f"Weather API response: {x}")

    if x.get("cod") != "404":
        y = x.get("main", {})
        current_temperature = y.get("temp", "N/A")
        current_pressure = y.get("pressure", "N/A")
        current_humidity = y.get("humidity", "N/A")
        z = x.get("weather", [{}])
        weather_description = z[0].get("description", "N/A")
        speak(f"Temperature: {current_temperature - 273.15:.2f}°C \nPressure: {current_pressure} hPa \nHumidity: {current_humidity}% \nDescription: {weather_description}")
    else:
        speak("City Not Found")

def getNews():
    api_key = "3414a8234063497ba810c1c872058bf8"
    main_url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(main_url)
    articles = response.json()["articles"]
    results = []
    for article in articles:
        results.append(article["title"])
    for i, result in enumerate(results):
        speak(f"News {i + 1}: {result}")

def tellJoke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "What do you call fake spaghetti? An impasta!",
    ]
    speak(random.choice(jokes))

def openApplication(app_name):
    if 'notepad' in app_name:
        os.system('notepad')
    elif 'calculator' in app_name:
        os.system('calc')
    else:
        speak("Application not available")

def createFile(file_name):
    with open(file_name, 'w') as file:
        file.write("")  # Create an empty file
    speak(f"{file_name} has been created.")

def deleteFile(file_name):
    try:
        os.remove(file_name)
        speak(f"{file_name} has been deleted.")
    except FileNotFoundError:
        speak(f"{file_name} not found.")

def renameFile(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        speak(f"{old_name} has been renamed to {new_name}.")
    except FileNotFoundError:
        speak(f"{old_name} not found.")

#  controlling the volume through voice 


from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def setVolume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    speak(f"Volume set to {level} percent.")

def increaseVolume():
    setVolume(min(100, getCurrentVolume() + 10))

def decreaseVolume():
    setVolume(max(0, getCurrentVolume() - 10))

def getCurrentVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return int(volume.GetMasterVolumeLevelScalar() * 100)


#  command for wifi control 

import os

def connectToWiFi(network_name):
    command = f'netsh wlan connect name="{network_name}"'
    os.system(command)
    speak(f"Attempting to connect to {network_name}.")
    
    # Verify connection
    result = os.system(command)
    if result == 0:
        speak(f"Successfully connected to {network_name}.")
    else:
        speak(f"Failed to connect to {network_name}. Please check the network name and try again.")

def disconnectFromWiFi():
    command = 'netsh wlan disconnect'
    os.system(command)
    
    # Verify disconnection
    result = os.system(command)
    if result == 0:
        speak("Successfully disconnected from Wi-Fi.")
    else:
        speak("Failed to disconnect from Wi-Fi. Please try again.")


#  application management

def closeApplication(app_name):
    os.system(f'taskkill /im {app_name}.exe /f')
    speak(f"{app_name} has been closed.")

#  for getting the system information 

import psutil

def getSystemInfo():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 * 1024 * 1024)  # Convert to GB
    used_memory = memory_info.used / (1024 * 1024 * 1024)  # Convert to GB
    speak(f"CPU Usage: {cpu_usage}%")
    speak(f"Memory Usage: {used_memory:.2f} GB of {total_memory:.2f} GB")


def handleCommand(query):
    print(f"Handling command: {query}")  # Debugging line
    if 'open youtube' in query:
        speak('Opening YouTube')
        webbrowser.open("youtube.com")
    elif 'open google' in query:
        speak('Opening Google')
        webbrowser.open("google.com")
    elif 'create file' in query:
        speak("What should be the file name?")
        file_name = takeCommand()
        createFile(file_name)
    elif 'delete file' in query:
        speak("What is the name of the file to delete?")
        file_name = takeCommand()
        deleteFile(file_name)
    elif 'rename file' in query:
        speak("What is the old file name?")
        old_name = takeCommand()
        speak("What should be the new file name?")
        new_name = takeCommand()
        renameFile(old_name, new_name)
    elif 'increase volume' in query:
        increaseVolume()
    elif 'decrease volume' in query:
        decreaseVolume()
    elif 'connect to wifi' in query:
        speak("What is the Wi-Fi network name?")
        network_name = takeCommand()
        connectToWiFi(network_name)
    elif 'disconnect wifi' in query:
        disconnectFromWiFi()
    elif 'close application' in query:
        speak("Which application would you like to close?")
        app_name = takeCommand()
        closeApplication(app_name)
    elif 'system info' in query:
        getSystemInfo()
    elif 'shutdown' in query:
        os.system("shutdown /s /t 1")
    elif 'restart' in query:
        os.system("shutdown /r /t 1")
    elif 'play music' in query:
        music_dir = 'path_to_your_music_directory'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")
    elif 'open application' in query:
        speak("Which application would you like to open?")
        app_name = takeCommand()
        openApplication(app_name)
    elif 'connect to wifi' in query:
        speak("Which network should I connect to?")
        network_name = takeCommand()
        connectToWiFi(network_name)
    elif 'disconnect from wifi' in query:
        disconnectFromWiFi()
    else:
        speak('Sorry, I did not understand that command.')


if __name__ == "__main__":
    speak("System is ready. Start speaking...")
    while True:
        query = takeCommand()
        if query == "none":
            continue
        handleCommand(query)
