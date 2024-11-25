# Imports go at the top
from microbit import *
import neopixel
import random
import time
import log
import math

def main():
    np = neopixel.NeoPixel(pin1, 6)
    np.clear()
    np.show()

    yellow = (255,255,0)
    orange = (255,69,0)
    blue  = (0,0,255)
    red   =(255,0,0)
    # odsud
    
    np[4] = orange
    np[5] = yellow
    np[0]=  blue
    np[3]=  red
    
    # sem
    
    np.show()   

if __name__ == '__main__':
    main()
    display.show(Image.HEART)
