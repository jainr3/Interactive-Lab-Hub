
#Wizard of Odds Blackjack Program

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import qwiic_led_stick
import time
import qwiic_i2c
import qwiic_button
import urllib, urllib.request, urllib.parse, subprocess

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

def build_blackjack_strategy():
   # Encode the blackjack table into 2 dictionaries
   blackjack_strategy = dict()
   numerical_cards = {"TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9}
   all_cards = {"ACE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10}
   numerical_sums = list(range(5, 22))
   # ACE-X pattern
   for x, x_num in numerical_cards.items():
      for y, y_num in all_cards.items():
         z = "H"
         if (x_num in [2, 3, 4, 5, 6, 7] and y_num in [5, 6]) or (x_num in [4, 5, 6, 7] and y_num in [4]) or (x_num in [6, 7] and y_num in [3]):
            z = "D"
         elif (x_num in [8, 9, 10]) or (x_num in [7] and y_num in [2, 7, 8]):
            z = "S"
         blackjack_strategy[(y, "ACE", x)] = z
  
   # DOUBLE pattern X-X
   for x, x_num in all_cards.items():
      for y, y_num in all_cards.items():
         z = "H"
         if (x_num in [1, 8]) or (x_num in [7, 8, 9] and y_num in [2, 3, 4, 5, 6]) or (x_num in [6] and y_num in [3, 4, 5, 6]) or (x_num in [7, 8] and y_num in [7]) or (x_num in [9] and y_num in [8, 9]) or (x_num in [2, 3] and y_num in [4, 5, 6, 7]):
            z = "P"
         elif (x_num in [10] or (x_num in [9] and y_num in [7, 10, 1])):
            z = "S"
         elif (x_num in [5] and y_num in [2, 3, 4, 5, 6, 7, 8, 9]):
            z = "D"
      
         blackjack_strategy[(y, x, x)] = z
  
   # Remaining numerical sums
   for x_num in numerical_sums:
      for y, y_num in all_cards.items():
         z = "H"
         if (x_num in [17, 18, 19, 20, 21]) or (x_num in [13, 14, 15, 16] and y_num in [2, 3, 4, 5, 6]) or (x_num in [12] and y_num in [4, 5, 6]):
            z = "S"
         elif (x_num in [16] and y_num in [9, 10, 1]) or (x_num in [15] and y_num in [10]):
            z = "Su"
         elif (x_num in [9] and y_num in [3, 4, 5, 6]) or (x_num in [10, 11] and y in [2, 3, 4, 5, 6, 7, 8, 9]) or (x_num in [11] and y_num in [10]):
            z = "D"

         blackjack_strategy[(y, x_num)] = z
   
   return blackjack_strategy

def google_tts(words):
  url = f"http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={words}&tl=en"
  subprocess.call(['/usr/bin/mplayer', '-ao', 'alsa', '-really-quiet', '-noconsolecontrols', url])

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      print("Unable to access webcam.")


# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
# Load Labels:
labels=[]
f = open("labels.txt", "r")
for line in f.readlines():
   if(len(line)<1):
      continue
   labels.append(line.split(' ')[1].strip())

# Specific vars for blackjack
dealer_card = ""
player_cards = []
num_scanned_cards = 0 # will give predictions after 3 cards have been scanned in
recommended_action = ""
cards_mapping = {"TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10, "JACK": 10, "QUEEN": 10, "KING": 10, "ACE": 11}

my_stick = qwiic_led_stick.QwiicLEDStick()
red_button = qwiic_button.QwiicButton(0x6F)
green_button = qwiic_button.QwiicButton(0x5B)
green_button.LED_off()
red_button.LED_off()
my_stick.LED_off()
brightness = 100

print("Building strategy")
blackjack_strategy = build_blackjack_strategy()

if my_stick.begin() == False:
   print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
      file=sys.stderr)
   exit()
print("\nLED Stick ready!")
my_stick.LED_off()

if red_button.begin() == False:
   print("\nThe Qwiic Button 1 isn't connected to the system. Please check your connection", \
      file=sys.stderr)
   exit()
if green_button.begin() == False:
   print("\nThe Qwiic Button 2 isn't connected to the system. Please check your connection", \
      file=sys.stderr)
   exit()

print("\nButton's ready!")

while(True):
   if webCam:
      ret, img = cap.read()

   # Check if button 1 is pressed
   if red_button.is_button_pressed() == True:
      print("Red button is pressed!")
      red_button.LED_on(brightness)
      # Reset the counts...
      dealer_card = ""
      player_cards = []
      num_scanned_cards = 0
      recommended_action = ""
      my_stick.LED_off()
   
   # Check if button2 is pressed
   if green_button.is_button_pressed() == True:
      print("Green button is pressed!")
      green_button.LED_on(brightness)

      rows, cols, channels = img.shape
      data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

      size = (224, 224)
      img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
      #turn the image into a numpy array
      image_array = np.asarray(img)

      # Normalize the image
      normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
      # Load the image into the array
      data[0] = normalized_image_array

      # run the inference
      prediction = model.predict(data)
      card = labels[np.argmax(prediction)]
      print("I think its a:", card)

      if card != "BACKGROUND":
         if card in ["JACK", "QUEEN", "KING"]:
            card = "TEN" # remap these
         if num_scanned_cards == 0:
            dealer_card = card
         else:
            player_cards.append(card)
         
         num_scanned_cards += 1

         if num_scanned_cards >= 3:
            # Test all the special cases first, before trying the sum based strategy
            if (dealer_card, player_cards[0], player_cards[1]) in blackjack_strategy and len(player_cards) == 2:
               recommended_action = blackjack_strategy[(dealer_card, player_cards[0], player_cards[1])]
            else:
               possible_sums = []
               # First take the literal sum and filter out later if it is higher than 21
               possible_sums.append(sum([cards_mapping[x] for x in player_cards]))

               # Then take all the combinations of sums considering if player has ACE(s)
               for ace_num in range(player_cards.count("ACE")):
                  possible_sums.append(possible_sums[-1] - 10)
               
               possible_sums = [x for x in possible_sums if x <= 21]
               print("The possible sums are", possible_sums)

               if len(possible_sums) >= 1:
                  # Do the simple strategy lookup
                  # Also, more complex strategy for multiple sums... for simplicity just take the higher sum 
                  # eg. A-2-A
                  recommended_action = blackjack_strategy[(dealer_card, possible_sums[0])]   
               else:
                  # No sums possible, have to surrender
                  recommended_action = "Su"
            print("The recommended action is", recommended_action, "for dealer card", dealer_card, "and player cards", player_cards)    
            full_action_mapping = {"H": "Hit", "S": "Stand", "D": "Double", "P": "Split", "Su": "Surrender"}
            google_tts(full_action_mapping[recommended_action])
   
   # Depending on the index, set a specific color for prediction # TODO
   if recommended_action == "H":
      my_stick.LED_off()
      my_stick.set_single_LED_color(10, 0, 255, 0)
      my_stick.set_single_LED_color(9, 0, 255, 0)
   elif recommended_action == "S":
      my_stick.LED_off()
      my_stick.set_single_LED_color(8, 255, 0, 0)
      my_stick.set_single_LED_color(7, 255, 0, 0)
   elif recommended_action == "D":
      my_stick.LED_off()
      my_stick.set_single_LED_color(6, 0, 255, 0)
      my_stick.set_single_LED_color(5, 0, 255, 0)
   elif recommended_action == "P":
      my_stick.LED_off()
      my_stick.set_single_LED_color(4, 0, 255, 0)
      my_stick.set_single_LED_color(3, 0, 255, 0)
   elif recommended_action == "Su":
      my_stick.LED_off()
      my_stick.set_single_LED_color(2, 255, 0, 0)
      my_stick.set_single_LED_color(1, 255, 0, 0)

   time.sleep(0.1)
   green_button.LED_off()
   red_button.LED_off()

   if webCam:
      if sys.argv[-1] == "noWindow":
         cv2.imwrite('detected_out.jpg',img)
         continue
      cv2.imshow('detected (press q to quit)',img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         cap.release()
         break
   else:
      break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
