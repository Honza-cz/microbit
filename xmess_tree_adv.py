# Imports go at the top
from microbit import *
import neopixel
import random
import time

main_colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128),
               (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (0, 0, 0)]


def basic(np, context, main_colors):
    if not context:
        it = iter(main_colors)
        c = next(it)
        context = (it, True, 0, 0, c)

    color_iterator, regular, last_time_tick, diod_index, color = context

    current_time_ms = time.ticks_ms()
    next_diod_index = diod_index
    if current_time_ms > (last_time_tick + 200):
        try:
            np[diod_index] = color
            np.show()

            if regular:
                next_diod_index = diod_index + 1

                if next_diod_index > 5:
                    color = next(color_iterator)
                    regular = not regular
                    next_diod_index = diod_index
            else:
                next_diod_index = diod_index - 1
                if next_diod_index < 0:
                    color = next(color_iterator)
                    regular = not regular
                    next_diod_index = 0
        except StopIteration:
            color_iterator = iter(main_colors)
            next_diod_index = diod_index
        last_time_tick = current_time_ms

    return (color_iterator, regular, last_time_tick, next_diod_index, color)


def glow(np, context):
    if not context:
        context = (True, 0, 0, 0)

    regular, last_time_tick, color_value, rgb_index = context

    current_time_ms = time.ticks_ms()
    if current_time_ms > (last_time_tick + 5):
        for diod_index in range(6):
            if rgb_index == 0:
                np[diod_index] = (color_value, 0, 0)
            elif rgb_index == 1:
                np[diod_index] = (0, color_value, 0)
            elif rgb_index == 2:
                np[diod_index] = (0, 0, color_value)

        np.show()

        if regular:
            if color_value + 1 <= 255:
                color_value += 1
            else:
                regular = not regular
                color_value -= 1

        else:
            if color_value - 1 >= 0:
                color_value -= 1
            else:
                regular = not regular
                color_value += 1
                if (rgb_index + 1) < 2:
                    rgb_index += 1
                else:
                    rgb_index = 0

        last_time_tick = current_time_ms

    return (regular, last_time_tick, color_value, rgb_index)


def main():
    np = neopixel.NeoPixel(pin1, 6)
    np.clear()
    np.show()

    x = 0
    y = 0
    l = 9

    context = None

    while(True):
        # context = basic(np, context, main_colors)
        context = glow(np, context)
        # display.set_pixel(x,y,l)
        # x+=1
        # if (x>4):
        #     x=0
        #     y+=1
        #     if (y>4):
        #         y=0
        #         if l==0:
        #             l=9
        #         else:
        #             l=0


if __name__ == '__main__':
    main()
    display.show(Image.HEART)
