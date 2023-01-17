# Imports go at the top
from microbit import *
import neopixel
import random

def random_fill():
    for d in range(6):
        np[d]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        np.show()
        sleep(200)
    for d in reversed(range(6)):
        np[d]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        np.show()
        sleep(200)

def color_fill(np, rgb, diods):
    for d in diods:
        np[d] = rgb
        np.show()
        sleep(500)

def main():
    main_colors = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,0),(0,255,128),(0,255,255),(0,128,255),(0,0,255),(128,0,255),(255,0,255),(255,0,128)]
    np= neopixel.NeoPixel(pin1,6)
    np.clear()
    np.show()

    regular = True
    color_iterator = iter(main_colors)
    while True:
        display.scroll(temperature())
        try:
            if regular:
                color_fill(np, next(color_iterator), range(6))
            else:
                color_fill(np, next(color_iterator), reversed(range(6)))
            regular = not regular
        except StopIteration:
            color_iterator = iter(main_colors)

if __name__ == '__main__':
    main()

