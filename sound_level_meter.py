from microbit import *
from time import sleep_us
from machine import time_pulse_us
import random
import neopixel


def color_fill(np, rgb, d):
    np[d] = rgb
    np.show()


def random_fill(np, diods):
    for d in diods:
        np[d] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.show()
    for d in diods:
        np[d] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.show()


def diod_light_rand():
    r = random.randint(0, 2)
    if r == 0:
        return 255
    elif r == 1:
        return 128
    elif r == 2:
        return 0


one_step = 10


def rgb_diods(mic_level):
    div = 1
    if mic_level < one_step * 10:
        div = 20
    elif one_step < mic_level < 5 * one_step:
        div = 10
    else:
        div = 1

    r = diod_light_rand() // div
    g = diod_light_rand() // div
    b = diod_light_rand() // div

    for i in range(6):
        color_fill(np, (r, g, b), i)


def diods5x5(mic_level):
    brightness = []
    for y in range(5):
        level = one_step * (y + 1)
        if level == mic_level:
            brightness.insert(0, 1)
        elif mic_level > level + one_step:
            brightness.insert(0, 9)
        elif mic_level > level:
            brightness.insert(0, 3)
        else:
            brightness.insert(0, 0)

    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, brightness[y])


def reset_diods():
    for y in range(5):
        for x in range(5):
            display.set_pixel(x, y, 0)

    for i in range(6):
        color_fill(np, (0, 0, 0), i)


if __name__ == '__main__':
    np = neopixel.NeoPixel(pin1, 6)
    np.clear()
    np.show()
    np.clear()
    np.show()

    beat = False
    counter = 1
    reset_counter = 1

    while True:
        if button_a.was_pressed():
            one_step += 1
        if button_b.was_pressed() and one_step > 0:
            one_step -= 1

        mic_level = microphone.sound_level()
        if mic_level > 0:
            beat = True
            reset_counter = 1
            if counter % 30 == 0:
                counter = 1
                rgb_diods(mic_level)
            else:
                counter += 1
            diods5x5(mic_level)

        else:
            if reset_counter % 1000 == 0 and beat:
                reset_counter = 1
                beat = False

                reset_diods()
            else:
                reset_counter += 1
