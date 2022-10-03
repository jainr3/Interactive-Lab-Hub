#!/usr/bin/env python3
import sys
import os
import wave
import json
import subprocess
import time
import random
from pygame import mixer
import threading

import board
from adafruit_apds9960.apds9960 import APDS9960

# This is the scripted version of the interaction that makes it easier to show what it might look like if the STT was more reliable

# Change this if the hardware card changes for the speaker (check using `arecord -l`)
CARD = "1"
with open('jokes.json', 'r') as f:
    JOKES = json.load(f)

def text_to_speech(words):
    #subprocess.call(["flite", "-voice", "slt", "-t" "'Hello Rahul! You are looking fantastic today!'"])
    # https://stackoverflow.com/a/64796337
    ps = subprocess.run(["espeak", "-ven+f2", "-k5", "-s150", "--stdout", words], check=True, capture_output=True)
    output = subprocess.run(["aplay", "-D", "plughw:" + CARD + ",0"], input=ps.stdout, capture_output=True)


print("Done with setup")
def scenario_1(): 
    # Scenario 1:
    # User enters the elevator and says OK ELE
    input("Press enter to go to next command\n")
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says PLAY MUSIC
    input("Press enter to go to next command\n")
    words = "The songs of the day are Despacito, Secrets, and Take You There. Select a song number."
    text_to_speech(words)
    # User selects a song number (1)
    input("Press enter to go to next command\n")
    words = "Now playing song one"
    text_to_speech(words)
    mixer.init()
    mixer.music.load("music/despacito.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play()
    # User gestures twice over the sensor to increase the volume
    input("Press enter to go to next command\n")
    mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.25))
    mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.25))
    # User says OK ELE
    # User says pause music
    input("Press enter to go to next command\n")
    mixer.music.pause()

def scenario_2():
    # Scenario 2:
    # User gestures over the sensor on the outside to summon elevator to go up
    input("Press enter to go to next command\n")
    words = "Going up"
    text_to_speech(words)
    # User enters the elevator and says OK ELE
    input("Press enter to go to next command\n")
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says SELECT FLOOR
    input("Press enter to go to next command\n")
    words = "What floor do you want to go to?" 
    text_to_speech(words)
    # User says Floor two
    input("Press enter to go to next command\n")
    words = "Got it. Floor two. Any others?" 
    text_to_speech(words)
    # User2 says floor five
    input("Press enter to go to next command\n")
    words = "Got it. Floor seven. Any others?" 
    text_to_speech(words)
    # Users say NO
    input("Press enter to go to next command\n")
    words = "Great. Going to floors two and seven." 
    text_to_speech(words)

def scenario_3():
    # Scenario 3:
    # User enters the elevator and says OK ELE
    input("Press enter to go to next command\n")
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says tell me a joke
    input("Press enter to go to next command\n")
    joke_idx = random.randint(0, len(JOKES) - 1)
    words = "Here's a joke" + JOKES[joke_idx]["setup"]
    text_to_speech(words)
    # User gives some attempt or thinks, then it delivers punchline
    input("Press enter to go to next command\n")
    words = JOKES[joke_idx]["punchline"]
    text_to_speech(words)

def scenario_4():
    # Scenario 4:
    # User enters the elevator where there are already 2-3 people
    people_count = 3
    input("Press enter to go to next command\n")
    text_to_speech("Detected " + str(people_count) + " people. Entering express-mode, Please speak any special floor requests now")
    # User says floor two
    input("Press enter to go to next command\n")
    text_to_speech("Ok will stop on floor two. Any others?")
    # User says no
    input("Press enter to go to next command\n")
    text_to_speech("Ok got it.")

scenario_1()
#scenario_2()
#scenario_3()
#scenario_4()