
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)
espeak -ven+f2 -k5 -s150 --stdout  "Hello Rahul! You are looking great today!" | aplay
 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Hello Rahul! You are looking great today!" | festival --tts

#adapted from https://learn.adafruit.com/speech-synthesis-on-the-raspberry-pi/speak-easier-flite

flite -voice slt -t "Hello Rahul! You are looking great today!"

#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Hello Rahul! You are looking great today!"
 
# from https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

pico2wave -w hellorahul.wav "Hello Rahul! You are looking great today!" && aplay hellorahul.wav

