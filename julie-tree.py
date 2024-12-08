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
    purple=(128,0,128)
    green=(0,255,0)
    # odsud
    


    np[0]=  blue
    np.show()  
    sleep(1000)
    np[1]=  purple
    np.show()  
    sleep(1000)
    np[2]=  green
    np.show()  
    sleep(1000)    
    np[3]=  red
    np.show()  
    sleep(1000)
    np[4] = orange
    np.show()  
    sleep(1000)
    np[5] = yellow
    np.show()  
    sleep(1000)
    # sem
    
    np.show()   

if __name__ == '__main__':
    main()
    display.show(Image.HEART)
