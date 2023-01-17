from microbit import *
from time import sleep_us
from machine import time_pulse_us
import random
import utime
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
        """
        车头超声波读取距离
        :param unit:检测距离单位 0 厘米 1 英尺
        :return:距离
        """
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


def turn_random():
    r = random.randint(0, 50)
    if random.getrandbits(1):
        ct.set_motors_speed(-r, r)
        ct.set_car_light(left, 0, 0, 255)
        ct.set_car_light(right, 0, 255, 0)
        color_fill(np, (0, 0, 255), 0)
        color_fill(np, (0, 255, 0), 1)
    else:
        ct.set_motors_speed(r, -r)
        ct.set_car_light(left, 0, 255, 0)
        ct.set_car_light(right, 0, 0, 255)
        color_fill(np, (0, 255, 0), 0)
        color_fill(np, (0, 0, 255), 1)


index = 0
cb_size = 100

movement = []


def add_new_movement(v):
    global movement
    movement.append(v)
    if len(movement) > cb_size:
        movement = movement[1:]


def any_movement():
    for m in movement:
        if m:
            return True
    return False


def color_fill(np, rgb, d):
    np[d] = rgb
    np.show()


none = 0
turning = 1
straight_fast = 2
straight_slow = 3
backwards = 4

current_action = none
action_end = 0
z_strength = -1000
if __name__ == '__main__':
    ct = CUTEBOT()
    np = neopixel.NeoPixel(pin15, 2)
    np.clear()
    np.show()
    ct.set_motors_speed(0, 0)
    ct.set_car_light(left, 0, 0, 0)
    ct.set_car_light(right, 0, 0, 0)
    display.scroll("OK")
    while(True):
        if current_action == turning:
            if utime.ticks_diff(action_end, utime.ticks_ms()) > 0:
                continue
            else:
                ct.set_motors_speed(0, 0)

        if current_action == backwards:
            display.show("X")
            if utime.ticks_diff(action_end, utime.ticks_ms()) > 0:
                display.show("b")
                continue
            else:
                turn_random()
                display.show("t")
                current_action = turning
                action_end = utime.ticks_add(utime.ticks_ms(), 200)
                continue
        else:
            if 0 < accelerometer.get_z() < 50:
                add_new_movement(False)
            else:
                add_new_movement(True)

        if not any_movement():
            ct.set_car_light(left, 255, 0, 0)
            ct.set_car_light(right, 255, 0, 0)
            ct.set_motors_speed(-20, -20)
            color_fill(np, (255, 0, 0), 0)
            color_fill(np, (255, 0, 0), 1)
            action_end = utime.ticks_add(utime.ticks_ms(), 500)
            current_action = backwards
            display.show("B")
            movement = []
            continue

        distance = ct.get_distance()
        if distance > 50:
            display.show("R")
            ct.set_motors_speed(50, 50)
            ct.set_car_light(left, 0, 255, 0)
            ct.set_car_light(right, 0, 255, 0)
            color_fill(np, (0, 255, 0), 0)
            color_fill(np, (0, 255, 0), 1)
        elif distance < 20:
            display.show("O")
            turn_random()
            current_action = turning
            action_end = utime.ticks_add(utime.ticks_ms(), 200)
        elif 50 > distance > 20:
            display.show("P")
            ct.set_motors_speed(20, 20)
            ct.set_car_light(left, 0, 0, 255)
            ct.set_car_light(right, 0, 0, 255)
            color_fill(np, (0, 0, 255), 0)
            color_fill(np, (0, 0, 255), 1)
