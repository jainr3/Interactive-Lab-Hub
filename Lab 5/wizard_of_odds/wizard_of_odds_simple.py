import qwiic_led_stick
import time
import qwiic_i2c
import qwiic_button
import urllib, urllib.request, urllib.parse, subprocess

# Defining a simple scenario to test acting it out
my_stick = qwiic_led_stick.QwiicLEDStick()
red_button = qwiic_button.QwiicButton(0x6F)
green_button = qwiic_button.QwiicButton(0x5B)
green_button.LED_off()
red_button.LED_off()
my_stick.LED_off()

brightness = 100

def google_tts(words):
  url = f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={words}&tl=en"
  subprocess.call(['/usr/bin/mplayer', '-ao', 'alsa', '-really-quiet', '-noconsolecontrols', url])

input("Press enter to go to next command\n")
# dealer's card is scanned, green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#1), green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#2), green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

time.sleep(0.5)
# wizard does the calculation and lights up action (stand)
my_stick.set_single_LED_color(8, 255, 0, 0)
my_stick.set_single_LED_color(7, 255, 0, 0)
google_tts("Stand")

input("Press enter to go to next command\n")
# user presses the red button to reset wizard
my_stick.LED_off()
red_button.LED_on(brightness)
time.sleep(1)
red_button.LED_off()

input("Press enter to go to next command\n")
# dealer's card is scanned, green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#1), green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#2), green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

time.sleep(0.5)
# wizard does the calculation and lights up action (hit)
my_stick.set_single_LED_color(10, 0, 255, 0)
my_stick.set_single_LED_color(9, 0, 255, 0)
google_tts("Hit")

input("Press enter to go to next command\n")
# user's card is scanned (#3), green button lights up
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()
my_stick.LED_off()

time.sleep(0.5)
# wizard does the calculation and lights up action (stand)
my_stick.set_single_LED_color(8, 255, 0, 0)
my_stick.set_single_LED_color(7, 255, 0, 0)
google_tts("Stand")

input("Press enter to go to next command\n")
# user presses the red button to reset wizard
my_stick.LED_off()
red_button.LED_on(brightness)
time.sleep(1)
red_button.LED_off()