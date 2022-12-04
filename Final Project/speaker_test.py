
# simple speaker test

import subprocess, threading
from queue import Queue
import pacman_sensors

#subprocess.call(["aplay", "sounds/pacman_beginning.wav"])

speaker_queue = Queue()

speaker_thread = threading.Thread(target=pacman_sensors.output_sound, args=(speaker_queue,))
speaker_thread.start()

speaker_queue.put(pacman_sensors.PACMAN_BEGINNING)