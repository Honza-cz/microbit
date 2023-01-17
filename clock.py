from microbit import *
import time
from math import *


start_ticks = time.ticks_ms()
started_at = (23 * 3600) + (52 * 60)
while True:
     if button_a.was_pressed():
          started_at += 60
     if button_b.was_pressed():
          started_at -= 60
     diff = time.ticks_diff(time.ticks_ms(), start_ticks)
     seconds = diff / 1000 + started_at
     h = floor(seconds / 3600)
     m = (seconds - h * 3600) // 60
     display.scroll(str(h % 24) + ":" + "{:02d}".format(int(m)))
