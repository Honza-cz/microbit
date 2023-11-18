from microbit import *
import time
from math import *
import speech


start_ticks = time.ticks_ms()
started_at = (00 * 3600) + (00 * 60)

setup_mode=0
too_hot = False
too_cold = False

while True:
    if pin_logo.is_touched():
        setup_mode=time.ticks_ms()

    if (setup_mode+20000)>time.ticks_ms():
        display.show("S")
        increment = 60
        if pin_logo.is_touched():
              increment = increment*60
        if button_a.was_pressed():
              started_at += increment
        elif button_b.was_pressed():
              started_at -= increment         
    else: 
        diff = time.ticks_diff(time.ticks_ms(), start_ticks)
        seconds = diff / 1000 + started_at
        h = floor(seconds / 3600)
        m = (seconds - h * 3600) // 60
        display.scroll(str(h % 24) + ":" + "{:02d}".format(int(m)))
        display.show('-')
        display.scroll(str(temperature())+'C')
        if (temperature()>29 and not too_hot):
            too_hot=True
            speech.say('Too hot!')
        elif (temperature()<20 and not too_cold):
            too_cold=True
            speech.say('Too cold!')
        
        if 20<temperature()<29 :
            too_cold=False
            too_hot=False
