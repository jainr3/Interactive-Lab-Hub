
# simple speaker test

import subprocess, threading
from queue import Queue
import pacman_sensors

#subprocess.call(["aplay", "sounds/pacman_beginning.wav"])
'''
speaker_queue = Queue()

speaker_thread = threading.Thread(target=pacman_sensors.output_sound, args=(speaker_queue,))
speaker_thread.start()

speaker_queue.put(pacman_sensors.PACMAN_BEGINNING)
'''

#basecmd = ["mplayer", "-ao", "alsa:device=bluetooth"]
#myfile = "sounds/pacman_beginning.wav"
#subprocess.call(basecmd + [myfile])

"""
import pygame
pygame.mixer.init()
pygame.mixer.music.load("sounds/pacman_beginning.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
"""

subprocess.call(["aplay", "-D", "bluealsa", "sounds/pacman_beginning.wav"])