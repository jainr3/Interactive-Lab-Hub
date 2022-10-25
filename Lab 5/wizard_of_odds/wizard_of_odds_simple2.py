import qwiic_led_stick
import time
import qwiic_i2c
import qwiic_button
import urllib, urllib.request, urllib.parse, subprocess, math

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
# dealer's card is scanned, green button lights up (ACE)
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#1), green button lights up (ACE)
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

input("Press enter to go to next command\n")
# user's card is scanned (#2), green button lights up (FIVE)
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

time.sleep(0.5)
# wizard does the calculation and lights up action (double)
my_stick.set_single_LED_color(6, 0, 255, 0)
my_stick.set_single_LED_color(5, 0, 255, 0)
google_tts("Double")

input("Press enter to go to next command\n")
# user's card is scanned (#3), green button lights up (FIVE)
green_button.LED_on(brightness)
time.sleep(1)
green_button.LED_off()

# BLACKJACK
def walking_rainbow(LED_stick, rainbow_length, LED_length, delay):
  red_array = [None] * LED_length
  blue_array = [None] * LED_length
  green_array = [None] * LED_length

  for j in range(0, rainbow_length):
    for i in range(0, LED_length):
      # There are n colors generated for the rainbow
      # The value of n determins which color is generated at each pixel
      n = i + 1 - j

      # Loop n so that it is always between 1 and rainbow_length
      if n <= 0:
        n = n + rainbow_length

      # The nth color is between red and yellow
      if n <= math.floor(rainbow_length / 6):
        red_array[i] = 255
        green_array[i] = int(math.floor(6 * 255 / rainbow_length * n))
        blue_array[i] = 0
      
      # The nth color is between yellow and green
      elif n <= math.floor(rainbow_length / 3):
        red_array[i] = int(math.floor(510 - 6 * 255 / rainbow_length * n))
        green_array[i] = 255
        blue_array[i] = 0
      
      # The nth color is between green and cyan
      elif n <= math.floor(rainbow_length / 2):
        red_array[i] = 0
        green_array[i] = 255
        blue_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 510))
      
      # The nth color is between blue and magenta
      elif n <= math.floor(5 * rainbow_length / 6):
        red_array[i] = int(math.floor(6 * 255 / rainbow_length * n - 1020))
        green_array[i] = 0
        blue_array[i] = 255
      
      # The nth color is between magenta and red
      else:
        red_array[i] = 255
        green_array[i] = 0
        blue_array[i] = int(math.floor(1530 - (6 *255 / rainbow_length * n)))

    # Set all the LEDs to the color values accordig to the arrays
    LED_stick.set_all_LED_unique_color(red_array, green_array, blue_array, LED_length)
    time.sleep(delay)

google_tts("Blackjack!!!")
walking_rainbow(my_stick, 40, 10, 0.05)



# user presses the red button to reset wizard
my_stick.LED_off()
#red_button.LED_on(brightness)
#time.sleep(1)
#red_button.LED_off()
