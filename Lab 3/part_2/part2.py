#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json
import subprocess
import speech_recognition as sr
import time
import random
from pygame import mixer
import threading

import board
from adafruit_apds9960.apds9960 import APDS9960


# Change this if the hardware card changes for the speaker (check using `arecord -l`)
CARD = "2"
with open('jokes.json', 'r') as f:
    JOKES = json.load(f)
SONGS = {"one": "despacito.mp3", "two": "secrets.mp3", "three": "take_you_there.mp3"}

def text_to_speech(words):
    #subprocess.call(["flite", "-voice", "slt", "-t" "'Hello Rahul! You are looking fantastic today!'"])
    # https://stackoverflow.com/a/64796337
    ps = subprocess.run(["espeak", "-ven+f2", "-k5", "-s150", "--stdout", words], check=True, capture_output=True)
    output = subprocess.run(["aplay", "-D", "plughw:" + CARD + ",0"], input=ps.stdout, capture_output=True)

def speech_to_text(filename):
    # This is the old way to do speech to text
  if not os.path.exists("model"):
      print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
      exit (1)

  wf = wave.open(filename, "rb")
  if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
      print ("Audio file must be WAV format mono PCM.")
      exit (1)

  model = Model("model")
  # You can also specify the possible word list
  #rec = KaldiRecognizer(model, wf.getframerate(), '["oh one two three four five six seven eight nine zero", "[unk]"]')
  rec = KaldiRecognizer(model, wf.getframerate(), '["oh one two three four five six seven eight nine zero"]')

  while True:
      data = wf.readframes(4000)
      if len(data) == 0:
          break
      if rec.AcceptWaveform(data):
          print(rec.Result())
      else:
          print(rec.PartialResult())

  result = json.loads(rec.FinalResult())
  return result

'''
TTS Shell command
#adapted from https://learn.adafruit.com/speech-synthesis-on-the-raspberry-pi/speak-easier-flite

flite -voice slt -t "Hello Rahul! You are looking great today!"

# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Hello Rahul! You are looking great today!" | aplay
'''

'''
STT Shell command
arecord -D hw:2,0 -f cd -c1 -r 44100 -d 5 -t wav part2.wav


'''

# Main script
# Original version: https://stackoverflow.com/a/53691763
trigger_word_active = False

r = sr.Recognizer()
r2 = sr.Recognizer()

# Words that sphinx should listen closely for. 0-1 is the sensitivity
# of the wake word.
keywords_trigger = [("alley", 1), ("ok alley", 1), ] # alley = ele

source = sr.Microphone()


i2c = board.I2C()

apds = APDS9960(i2c)
apds.enable_proximity = False
apds.enable_gesture = True


def callback(recognizer, audio):  # this is called from the background thread
        global trigger_word_active
        if not trigger_word_active:
            try:
                speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords_trigger)
                print(speech_as_text)

                # Look for your keyword in speech_as_text
                if "alley" in speech_as_text or "ok alley" in speech_as_text:
                    trigger_word_active = True
                    recognize_main()
                    trigger_word_active = False

            except sr.UnknownValueError:
                print("Oops! Didn't catch that")

def recognize_main():
    print("Recognizing Main...")
    # interpret the user's words however you normally interpret them
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    actions = [(x, 1) for x in ["floor", "music", "joke", "pause", "resume", "stop"]] # only need the keyword (the extra 3 pause/resume/stop here is for the music)
    floor_numbers = [(x, 1) for x in ["none", "no", "three"]] # keywords for the floor scenario that end the scenario
                                      #"one", "two", "three", "four", "five",]]# "six", "seven", "eight", "nine", "ten", 
                                      #"eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
                                      #"twentyone", "twentytwo", "twentythree", "twentyfour", "twentyfive", "twentysix"]]
    music = [(x, 1) for x in ['three']]# ["one", "two", "three"]]
    keywords = []

    start_time = time.time()
    action_selected = None
    done_with_interaction = False
    action_sub_selections = []
    while True:
        print("start")
        if action_selected == None:
            keywords = actions
        elif "floor" in action_selected:
            keywords = floor_numbers
            words = "What floor do you want to go to?" if len(action_sub_selections) == 0 else "Got it. Floor " + str(action_sub_selections[-1]) + " . Any others?"
            text_to_speech(words)
        elif "music" in action_selected:
            keywords = music
            words = "The songs of the day are Despacito, Secrets, and Take You There. Select a song number." if len(action_sub_selections) == 0 else "Now playing song " + str(action_sub_selections[-1])
            text_to_speech(words)
            if len(action_sub_selections) != 0:
                keywords = [] # done with the interaction
                mixer.init()
                mixer.music.load("music/" + SONGS[str(action_sub_selections[-1])])
                mixer.music.set_volume(0.5)
                mixer.music.play()
                done_with_interaction = True
        elif "joke" in action_selected:
            keywords = []
            joke_idx = random.randint(0, len(JOKES) - 1)
            words = "Here's a joke" + JOKES[joke_idx]["setup"]
            text_to_speech(words)
            time.sleep(2)
            words = JOKES[joke_idx]["punchline"]
            text_to_speech(words)
            done_with_interaction = True
        elif "pause" in action_selected:
            mixer.music.pause()
            done_with_interaction = True
        elif "resume" in action_selected:
            mixer.music.unpause()
            done_with_interaction = True
        elif "stop" in action_selected:
            mixer.music.stop()
            mixer.quit()
            done_with_interaction = True

        print(keywords)
        print(words)
        print(action_selected)
        print(action_sub_selections)
    
        if len(keywords) != 0 and not done_with_interaction:
            print("Listening for an action now.")
            while True:
                speech_as_text = None
                try:
                    audio_data = r2.listen(source)

                    speech_as_text = r2.recognize_sphinx(audio_data, keyword_entries=keywords).strip().split()[0] # take first word if multiple keywords detected
                    print("Detected", speech_as_text)
                    if action_selected == None:
                        action_selected = speech_as_text

                    elif "floor" in action_selected and "no" in speech_as_text or "none" in speech_as_text:
                        words = "Great. Selected floors"
                        for f in list(set(action_sub_selections)):
                            words += f + " "
                        text_to_speech(words)
                        done_with_interaction = True
                    else:
                        action_sub_selections.append(speech_as_text)
                except sr.UnknownValueError:
                    print("Didn't understand the subcommand.")
                    pass
                if speech_as_text != None:
                    break
            print("Done listening for an action.")
    
        if done_with_interaction:
            print("Interaction has completed.")
            break
        elif time.time() - start_time > 60: # this number of seconds is probably long enough for the interaction
            print("Interaction has timed out.")
            break


def start_recognizer():
    r.listen_in_background(source, callback)
    time.sleep(1000000)
    print("Recognizer done")

def volume_gestures():
    print("Started volume control thread")
    while True:
        gesture = apds.gesture()

        if gesture == 0x01:
            print("up")
            mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.25))
        elif gesture == 0x02:
            print("down")
            mixer.music.set_volume(max(0.0, mixer.music.get_volume() - 0.25))
        elif gesture == 0x03:
            print("left")
        elif gesture == 0x04:
            print("right")


# Main line starts here
thread = threading.Thread(target=volume_gestures)
thread.daemon = True
thread.start()

start_recognizer()



