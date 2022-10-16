# Code for Lab 4 Part 1 Prototype
import board
from rainbowio import colorwheel
import neopixel
import touchio
import time
import array
import math
import digitalio
from adafruit_apds9960.apds9960 import APDS9960

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
touch_A6 = touchio.TouchIn(board.A6)
touch_TX = touchio.TouchIn(board.TX)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

i2c = board.I2C()

apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE

# Make the 2 input buttons
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.DOWN

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.DOWN



passcode = "632UDT"


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

def light_pixel_no_wait(pixel, color):
    display_color(OFF, False)
    pixels[pixel] = color
    pixels.show()

def display_color(color, sleep=True):
    for i in range(10):
        pixels[i] = color
        pixels.show()
    if sleep:
        time.sleep(0.5)

def light_pixels_up_pattern(color, wait):
    # 4, 5 -> 3, 6 -> 2, 7 -> 1, 8 -> 0, 9
    for i in range(0, 5):
        light_pixel_no_wait(4-i, color)
        light_pixel_no_wait(5+i, color)
        time.sleep(wait)
    display_color(OFF)

def light_pixels_down_pattern(color, wait):
    # Reverse pattern of up
    for i in [4, 3, 2, 1, 0]:
        light_pixel_no_wait(4-i, color)
        light_pixel_no_wait(5+i, color)
        time.sleep(wait)
    display_color(OFF)

def light_pixels_left_pattern(color, wait):
    # 7 -> 6, 8 -> 5, 9 -> 4, 0 -> 3, 1 -> 2
    light_pixel_no_wait(7, color)
    time.sleep(wait)
    for i, j in [(6, 8), (5, 9), (4, 0), (3, 1)]:
        light_pixel_no_wait(i, color)
        light_pixel_no_wait(j, color)
        time.sleep(wait)
    light_pixel_no_wait(2, color)
    time.sleep(wait)
    display_color(OFF)

def light_pixels_right_pattern(color, wait):
    # Reverse pattern of left
    light_pixel_no_wait(2, color)
    time.sleep(wait)
    for i, j in [(3, 1), (4, 0), (5, 9), (6, 8)]:
        light_pixel_no_wait(i, color)
        light_pixel_no_wait(j, color)
        time.sleep(wait)
    light_pixel_no_wait(7, color)
    time.sleep(wait)
    display_color(OFF)

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

    gesture = apds.gesture()

    if gesture == 0x01:
        print("up")
        light_pixels_up_pattern(GREEN, 0.001)
        entered_combo += "U"
    elif gesture == 0x02:
        print("down")
        light_pixels_down_pattern(GREEN, 0.001)
        entered_combo += "D"
    elif gesture == 0x03:
        print("left")
        light_pixels_left_pattern(GREEN, 0.001)
        entered_combo += "L"
    elif gesture == 0x04:
        print("right")
        light_pixels_right_pattern(GREEN, 0.001)

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
    if touch_A6.value:
        print("A6 touched!")
        light_pixel(3, GREEN, 0.5)
        entered_combo += "6"
    if touch_TX.value:
        print("TX touched!")
        light_pixel(4, GREEN, 0.5)
        entered_combo += "T"



    if buttonA.value or buttonB.value:
        print("Button A/B pressed!")
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

