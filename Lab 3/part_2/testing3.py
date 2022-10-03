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

from adafruit_apds9960.apds9960 import APDS9960

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import


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
    time.sleep(4)
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says PLAY MUSIC
    time.sleep(4)
    words = "The songs of the day are Despacito, Secrets, and Take You There. Select a song number."
    text_to_speech(words)
    # User selects a song number (1)
    time.sleep(2)
    words = "Now playing song one"
    text_to_speech(words)
    mixer.init()
    mixer.music.load("music/despacito.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play()
    # User gestures twice over the sensor to increase the volume
    time.sleep(4)
    mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.25))
    mixer.music.set_volume(min(1.0, mixer.music.get_volume() + 0.25))
    # User says OK ELE
    # User says pause music
    time.sleep(10)
    mixer.music.pause()

def scenario_pre2():
  # User gestures over the sensor on the outside to summon elevator to go up
  time.sleep(2)
  words = "Going up"
  text_to_speech(words)

def scenario_2():
    # Scenario 2:
    # User enters the elevator and says OK ELE
    time.sleep(4)
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says SELECT FLOOR
    time.sleep(2)
    words = "What floor do you want to go to?" 
    text_to_speech(words)
    # User says Floor two
    time.sleep(3)
    words = "Got it. Floor two. Any others?" 
    text_to_speech(words)
    # User2 says floor seven
    time.sleep(3)
    words = "Got it. Floor seven. Any others?" 
    text_to_speech(words)
    # Users say NO
    time.sleep(3)
    words = "Great. Going to floors two and seven." 
    text_to_speech(words)

def scenario_3():
    # Scenario 3:
    # User enters the elevator and says OK ELE
    time.sleep(4)
    words = "Hi there. How can I help you today?"
    text_to_speech(words)
    # User says tell me a joke
    time.sleep(4)
    joke_idx = random.randint(0, len(JOKES) - 1)
    words = "Here's a joke" + JOKES[joke_idx]["setup"]
    text_to_speech(words)
    # User gives some attempt or thinks, then it delivers punchline
    time.sleep(4)
    words = JOKES[joke_idx]["punchline"]
    text_to_speech(words)

def scenario_4():
    # Scenario 4:
    # User enters the elevator where there are already 2-3 people
    people_count = 4
    time.sleep(4)
    text_to_speech("Detected " + str(people_count) + " people. Entering express-mode, Please speak any special floor requests now")
    # User says floor two
    time.sleep(3)
    text_to_speech("Ok will stop on floor two. Any others?")
    # User says no
    time.sleep(3)
    text_to_speech("Ok got it.")

#scenario_1()
#scenario_pre2()
#scenario_2()
#scenario_3()
#scenario_4()

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)
# pylint: enable=line-too-long

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)


scenario_number = 0 
# Scenario # mapping to functions
# 0 scenario_1()
# 1 scenario_pre2()
# 2 scenario_2()
# 3 scenario_3()
# 4 scenario_4()

while True:

    if buttonB.value and not buttonA.value:  # just button A pressed
      scenario_number += 1
      scenario_number %= 5
      draw.rectangle((0, 0, width, height), outline=0, fill=0)
      y = top
      scenario_string = "Scenario " + str(scenario_number)
      draw.text((x, y), scenario_string, font=font, fill="#0000FF")
      y += font.getsize(scenario_string)[1]

      # Display image.
      disp.image(image, rotation)
      time.sleep(1)
    if buttonA.value and not buttonB.value:  # just button B pressed
      if scenario_number == 0:
        scenario_1()
      elif scenario_number == 1:
        scenario_pre2()
      elif scenario_number == 2:
        scenario_2()
      elif scenario_number == 3:
        scenario_3()
      elif scenario_number == 4:
        scenario_4()