from microbit import *
import time
from math import *
import speech


def show_temp(too_hot, too_cold, scroll_delay):
    if show_temp:
        display.scroll(str(temperature()) + 'C', delay=scroll_delay)
        if (temperature() > 29 and not too_hot):
            too_hot = True
            speech.say('Too hot!')
        elif (temperature() < 20 and not too_cold):
            too_cold = True
            speech.say('Too cold!')

        if 20 < temperature() < 29:
            too_cold = False
            too_hot = False
    return too_hot, too_cold


last_tick = time.ticks_ms()
abs_last_timestamp = (00 * 3600) + (00 * 60)
setup_mode = 0
should_show_temp = False
too_hot = False
too_cold = False
scroll_delay = 120
while True:
    if pin_logo.is_touched():
        setup_mode = time.ticks_ms()

    if (setup_mode + 30000) > time.ticks_ms():
        display.show("S")
        increment = 60
        if pin_logo.is_touched():
            increment = increment * 60
        if button_a.was_pressed():
            abs_last_timestamp += increment
        elif button_b.was_pressed():
            abs_last_timestamp -= increment
    else:
        if button_a.was_pressed():
            should_show_temp = not should_show_temp
        if button_b.was_pressed():
            if scroll_delay == 120:
                scroll_delay = 70
            else:
                scroll_delay = 120

        now = time.ticks_ms()
        diff = time.ticks_diff(now, last_tick)
        last_tick = now
        seconds = diff / 1000 + abs_last_timestamp
        h = floor(seconds / 3600)
        m = (seconds - h * 3600) // 60
        abs_last_timestamp = seconds
        display.scroll(str(h % 24) + ":" + "{:02d}".format(int(m)), delay=scroll_delay)

        if should_show_temp:
            too_hot, too_cold = show_temp(too_hot, too_cold, scroll_delay)
