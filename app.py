
from flask import Flask,render_template,redirect,request
#from flask_sqlalchemy import SQLAlchemy
import warnings
warnings.filterwarnings('ignore')

import os
os.environ['DISPLAY'] = ':0'

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
import sys
import requests, json

listener = sr.Recognizer()

app = Flask("__name__")
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///queries.db"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#class Queries(db.Model):



sentence = ''
def talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source, None, 6)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        sentence = 'playing' + song
        return sentence
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        sentence = 'Current time is ' + time
        return sentence 
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'stop' in command:
        talk('Bye, have a good day')
        return redirect('/')
    else:
        talk('Please say the command again.')


@app.route('/')
def hello():
    return render_template("index.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/voice-active/')
def submit():
    while True:
        try:
            run_alexa()
        except UnboundLocalError:
            print("No command detected! Alexa has stopped working")
            talk('No command detected! Alexa has stopped working')
            return render_template("index.html")
            break
    

if __name__ =="__main__":
    app.run(debug=True)
