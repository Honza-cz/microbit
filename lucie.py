# Imports go at the top
from microbit import *
import music

while True:
    if button_a.was_pressed():
        song='cdeccdecefggefgggagfecgagfeccgcccgcc'
        music.play(list(song))
    if button_b.was_pressed():
        display.scroll(temperature())
