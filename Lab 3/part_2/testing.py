def speak(line):
    cmd = "./speak.sh \"{}\"".format(line)
    os.system(cmd)

#import vlc

#p = vlc.MediaPlayer("music/" + "despacito.mp3")
#p.play()

#import os
#os.system('mpg321 music/despacito.mp3')

'''
# Music player in python
# https://www.codesnail.com/how-to-make-music-player-in-python/
from pygame import mixer

mixer.init()
mixer.music.load("music/despacito.mp3")
mixer.music.set_volume(0.5)
mixer.music.play()

while True:
    print("Press 'p' to pause")
    print("Press 'r' to resume")
    print("Press 'v' set volume")
    print("Press 'e' to exit")

    ch = input("['p','r','v','e']>>>")

    if ch == "p":
        mixer.music.pause()
    elif ch == "r":
        mixer.music.unpause()
    elif ch == "v":
        v = float(input("Enter volume(0 to 1): "))
        mixer.music.set_volume(v)
    elif ch == "e":
        mixer.music.stop()
        break
'''

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_apds9960.apds9960 import APDS9960
from pygame import mixer

i2c = board.I2C()

apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

mixer.init()
mixer.music.load("music/take_you_there.mp3")
mixer.music.set_volume(0.5)
mixer.music.play()


# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE
print("Setup done")
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
