# Imports go at the top
from microbit import *
import music
import speech

while True:
    # display.show(Image.HEART)
    # sleep(400)
    if (button_a.was_pressed()):
        for x in range(5):
            for y in range(5):
                display.clear()
                display.set_pixel(y,x,9)
                sleep(50)
    if (button_b.was_pressed()):
        display.show(Image.HAPPY)
        speech.say('Happy new year 2023')
        audio.play(Sound.GIGGLE)
        
