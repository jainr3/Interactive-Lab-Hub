
#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say "Give me some numbers from 0 to 9 to add together."

arecord -D hw:2,0 -f cd -c1 -r 44100 -d 5 -t wav part1_stt.wav


python3 part1_stt.py part1_stt.wav
