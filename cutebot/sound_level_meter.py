from microbit import *
from time import sleep_us
from machine import time_pulse_us
import random
import neopixel

CUTEBOT_ADDR = 0x10
left = 0x04
right = 0x08


class CUTEBOT(object):
    def __init__(self):
        i2c.init()
        self.__pin_e = pin12
        self.__pin_t = pin8
        self.__pinL = pin13
        self.__pinR = pin14
        self.__pinL.set_pull(self.__pinL.PULL_UP)
        self.__pinR.set_pull(self.__pinR.PULL_UP)

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):
        if left_wheel_speed > 100 or left_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        if right_wheel_speed > 100 or right_wheel_speed < -100:
            raise ValueError('speed error,-100~100')
        left_direction = 0x02 if left_wheel_speed > 0 else 0x01
        right_direction = 0x02 if right_wheel_speed > 0 else 0x01
        left_wheel_speed = left_wheel_speed if left_wheel_speed > 0 else left_wheel_speed * -1
        right_wheel_speed = right_wheel_speed if right_wheel_speed > 0 else right_wheel_speed * -1
        i2c.write(CUTEBOT_ADDR, bytearray(
            [0x01, left_direction, left_wheel_speed, 0]))
        i2c.write(CUTEBOT_ADDR, bytearray(
            [0x02, right_direction, right_wheel_speed, 0]))

    def set_car_light(self, light: int, R: int, G: int, B: int):
        if R > 255 or G > 255 or B > 255:
            raise ValueError('RGB is error')
        i2c.write(CUTEBOT_ADDR, bytearray([light, R, G, B]))

    def get_distance(self, unit: int = 0):
        self.__pin_e.read_digital()
        self.__pin_t.write_digital(1)
        sleep_us(10)
        self.__pin_t.write_digital(0)
        ts = time_pulse_us(self.__pin_e, 1, 25000)

        distance = round(ts * 34 / 2 / 1000)
        if unit == 0:
            return distance
        elif unit == 1:
            return round(distance / 30.48, 2)

    def get_tracking(self):
        left = self.__pinL.read_digital()
        right = self.__pinR.read_digital()
        if left == 1 and right == 1:
            return 00
        elif left == 0 and right == 1:
            return 10
        elif left == 1 and right == 0:
            return 1
        elif left == 0 and right == 0:
            return 11
        else:
            print("Unknown ERROR")

    def set_servo(self, servo, angle):
        if servo > 2 or servo < 1:
            raise ValueError('select servo error,1,2')
        if angle > 180 or angle < 0:
            raise ValueError('angle error,0~180')
        i2c.write(CUTEBOT_ADDR, bytearray([servo + 4, angle, 0, 0]))


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


def rgb_diods():
    r = diod_light_rand()
    g = diod_light_rand()
    b = diod_light_rand()
    ct.set_car_light(left, r, g, b)
    ct.set_car_light(right, r, g, b)

    color_fill(np, (r, g, b), 0)
    color_fill(np, (r, g, b), 1)


one_step = 1


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

    ct.set_car_light(left, 0, 0, 0)
    ct.set_car_light(right, 0, 0, 0)

    color_fill(np, (0, 0, 0), 0)
    color_fill(np, (0, 0, 0), 1)


if __name__ == '__main__':
    ct = CUTEBOT()
    np = neopixel.NeoPixel(pin15, 2)
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
                rgb_diods()
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
