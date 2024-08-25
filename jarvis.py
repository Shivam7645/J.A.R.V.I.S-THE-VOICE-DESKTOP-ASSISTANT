import pyttsx3 as pt
import speech_recognition as sr
import datetime
import wikipedia 
import webbrowser
import random
import pyautogui as pi
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2
import os

engine = pt.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe(user_name=None):
    current_hour = datetime.datetime.now().hour
    greeting_messages = {
        "morning": ["Good Morning!", "Good Morning! I hope you're having a great day."],
        "afternoon": ["Good Afternoon!", "Hello there! It's a beautiful afternoon."],
        "evening": ["Good Evening!", "Good Evening! I hope you had a wonderful day."]
    }

    if 0 <= current_hour < 12:
        greeting = random.choice(greeting_messages["morning"])
    elif 12 <= current_hour < 18:
        greeting = random.choice(greeting_messages["afternoon"])
    else:
        greeting = random.choice(greeting_messages["evening"])

    if user_name:
        speak(f"{greeting}, {user_name}!")
    else:
        speak(greeting)
    
    speak("Ready to assist you. How can I help?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: \"{query}\"")

    except Exception as e:
        print("Say that again, please...")
        return "None"
    
    return query.lower()

def play_spotify_track(track_name):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
                                                       client_secret='your_client_secret',
                                                       redirect_uri='your_redirect_uri',
                                                       scope='user-library-read user-modify-playback-state'))

        results = sp.search(q=track_name, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[track_uri])
            print(f"Playing: {track_name}")
        else:
            print(f"Could not find the track: {track_name}")

    except Exception as e:
        print("Error playing Spotify track:", e)

def open_camera_and_capture_photo():
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            speak("Error opening the camera. Please make sure it is connected.")
            return

        speak("Camera opened. Smile and get ready for the photo!")

        # Capture a frame
        ret, frame = cap.read()

        # Save the captured frame as an image
        if ret:
            speak("Photo captured! Please enter a name for the photo:")
            name = takeCommand().lower()

            try:
                photo_path = os.path.join(os.getcwd(), f"{name}.png")
                cv2.imwrite(photo_path, frame)
                speak("Photo saved successfully.")
            except Exception as e:
                print("Error saving photo:", e)
                speak("Sorry, there was an error saving the photo.")

        # Release the camera
        cap.release()

    except Exception as e:
        print("Error opening camera and capturing photo:", e)
        speak("Sorry, there was an error opening the camera and capturing the photo.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()
        print(query)
        
        if 'jarvis' in query:
            print("Yes sir")
            speak("Yes sir")
            continue

        elif 'open google' in query:
            try:
                webbrowser.open('https://www.google.com')
            except Exception as e:
                print("Error opening Google:", e)

            speak("What do you want to search for?")
            qry = takeCommand().lower()

            if qry != 'none':
                try:
                    results = wikipedia.summary(qry, sentences=1)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as disambiguation_error:
                    print("Wikipedia Disambiguation Error:", disambiguation_error)
                    options = disambiguation_error.options
                    speak(f"The term '{qry}' is ambiguous. It may refer to: {', '.join(options)}. Please specify your search.")
                except wikipedia.exceptions.PageError as page_error:
                    print("Wikipedia Page Error:", page_error)
                    speak(f"Sorry, I couldn't find any information about '{qry}' on Wikipedia. Let me search the web for you.")
                    webbrowser.open(f"https://www.google.com/search?q={qry.replace(' ', '+')}")

        elif 'open youtube' in query:
            try:
                webbrowser.open('https://www.youtube.com')
                speak("What do you want to search for on YouTube?")
                search_query = takeCommand().lower()
                if search_query != 'none':
                    youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"
                    webbrowser.open(youtube_search_url)
            except Exception as e:
                print("Error opening YouTube:", e)

        elif 'open chat gpt' in query:
            try:
                webbrowser.open('https://www.chatgpt.com')
            except Exception as e:
                print("Error opening chat gpt:", e)

 
        elif "take a screenshot" in query:
            speak("Please enter a name for the screenshot:")
            name = takeCommand().lower()  # Directly take input from the user
            try:
                img = pi.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot saved")
            except Exception as e:
                print("Error taking screenshot:", e)
                speak("Sorry, there was an error taking the screenshot.")

        elif 'open spotify' in query:
            try:
                webbrowser.open('https://open.spotify.com')
            except Exception as e:
                print("Error opening Spotify:", e)

            speak("What song do you want to play on Spotify?")
            track_name = takeCommand().lower()
            if track_name != 'none':
                play_spotify_track(track_name)

        elif 'open paint' in query:
            npath = "https://www.microsoft.com/store/productId/9PCFS5B6T72H?ocid=pdpshare"
            webbrowser.open(npath)

        elif 'open camera' in query:
            open_camera_and_capture_photo()
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is{strTime}")
        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")
        elif"restart the system" in query:
            os.system("shutdown /r /t 5")
        elif "lock the system" in query:
            os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
        elif "hibernate the system" in query:
            os.system("rundll32.exe powrof.dll,SetSuspendState 0,1,0")
        elif 'type' in query:
            query = query.replace("type","")
            pi.typewrite(f"{query}",0.1)
        elif 'about my group members' in query:
            positive_remarks = {'Shivam': "Shivam is incredibly diligent and always brings fresh ideas to the table.",
        'Manish': "Manish has an exceptional ability to solve complex problems and is a great team player.",
        'Alok': "Alok's positive attitude and enthusiasm are contagious, making every project enjoyable.",
        'Ankit': "Ankit is a natural leader, guiding the team with his wisdom and expertise."
        }
            for member, remark in positive_remarks.items():
                speak(f"Let me tell you something good about {member}. {remark}")
        elif 'about our faculty' in query:
            faculty_remarks = {'Pratap Sir': "Pratap Sir has been a guiding light for us, providing invaluable insights and support throughout our journey.",
        'Rajesh Sir': "Rajesh Sir's mentorship has been instrumental in shaping our skills and motivating us to achieve our goals."
        }
            for advisor, remark in faculty_remarks.items():
                speak(f"I would like to express our gratitude towards {advisor}. {remark}")