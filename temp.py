# Imports go at the top
from microbit import *

def main():

    show_always = False
    is_compas_calibrated = False
    while True:
        if button_a.was_pressed() or show_always:
            display.scroll(temperature())
        if button_b.was_pressed():
            show_always = not show_always
        if pin_logo.is_touched() or show_always:
            if is_compas_calibrated:
                compass.calibrate()
                is_compas_calibrated=not is_compas_calibrate
            heading = compass.heading()
            if 0 <= heading < 30:
                display.scroll('N')
            elif 30 <= heading < 55:
                display.scroll('NE')
            elif 55 <= heading < 115:
                display.scroll('E')
            elif 115 <= heading < 165:
                display.scroll('SE')
            elif 165 <= heading < 205:
                display.scroll('S')
            elif 205 <= heading < 250:
                display.scroll('SW')
            elif 250 <= heading < 295:
                display.scroll('W')
            elif 295 <= heading < 335:
                display.scroll('NW')
            elif 225 <= heading <= 360:
                display.scroll('NW')
            else:
                display.scroll('?')
        sleep(200)

if __name__ == '__main__':
    main()

