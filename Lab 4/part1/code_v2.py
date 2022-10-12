# Code for Lab 4 Part 1 Prototype
import board
from rainbowio import colorwheel
import neopixel
import touchio
import time
import array
import math
import digitalio

try:
    from audiocore import RawSample
except ImportError:
    from audioio import RawSample
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass # not always supported by every board!

FREQUENCY = 255
SAMPLERATE = 8000 # 8000 samples/second, recommended!
# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for i in range(length):
 sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)
# Enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True
audio = AudioOut(board.SPEAKER)
sine_wave_sample = RawSample(sine_wave)
# A single sine wave sample is hundredths of a second long. If you set loop=False, it will play
# a single instance of the sample (a quick burst of sound) and then silence for the rest of the
# duration of the time.sleep(). If loop=True, it will play the single instance of the sample
# continuously for the duration of the time.sleep().


touch_A1 = touchio.TouchIn(board.A1)
touch_A2 = touchio.TouchIn(board.A2)
touch_A3 = touchio.TouchIn(board.A3)
touch_A4 = touchio.TouchIn(board.A4)
touch_A5 = touchio.TouchIn(board.A5)
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

passcode = "6325"


def color_chase(color, wait):
    for i in range(10):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    #time.sleep(0.5)

def light_pixel(pixel, color, wait):
    display_color(OFF)
    pixels[pixel] = color
    time.sleep(wait)
    pixels.show()

def display_color(color):
    for i in range(10):
        pixels[i] = color
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

entered_combo = ""

display_color(RED)
while True:
    # Main loop for processing input combinations    

    #if len(entered_combo) == 0:
    #    # Spin the lights around in a rainbow
    #    #rainbow_cycle(0.002)
    #    color_chase(YELLOW, 0.05)
    #    color_chase(OFF, 0.05)

    if touch_A1.value:
        print("A1 touched!")
        light_pixel(6, GREEN, 0.5)
        entered_combo += "1"
    if touch_A2.value:
        print("A2 touched!")
        light_pixel(7, GREEN, 0.5)
        entered_combo += "2"
    if touch_A3.value:
        print("A3 touched!")
        light_pixel(8, GREEN, 0.5)
        entered_combo += "3"
    if touch_A4.value:
        print("A4 touched!")
        light_pixel(1, GREEN, 0.5)
        entered_combo += "4"
    if touch_A5.value:
        print("A5 touched!")
        light_pixel(2, GREEN, 0.5)
        entered_combo += "5"
    if touch_A6.value:
        print("A6 touched!")
        light_pixel(3, GREEN, 0.5)
        entered_combo += "6"
    if touch_TX.value:
        print("TX touched!")
        if entered_combo == passcode:
            # Unlock successful
            display_color(GREEN)
            time.sleep(5)
            rainbow_cycle(0.002)
        else:
            display_color(RED)
            audio.play(sine_wave_sample, loop=True) # Play the single sine_wave sample continuously...
            time.sleep(1) # for the duration of the sleep (in seconds)
            audio.stop() # and then stop.
            time.sleep(3)
            rainbow_cycle(0.002)
        display_color(RED)
        entered_combo = ""


    time.sleep(0.04)

