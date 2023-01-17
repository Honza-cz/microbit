from microbit import *
from time import sleep_us
from machine import time_pulse_us
import random
import neopixel

CUTEBOT_ADDR = 0x10
left = 0x04
right = 0x08


class CUTEBOT(object):
    """基本描述

    Cutebot（酷比特）智能赛车

    """

    def __init__(self):
        i2c.init()
        self.__pin_e = pin12
        self.__pin_t = pin8
        self.__pinL = pin13
        self.__pinR = pin14
        self.__pinL.set_pull(self.__pinL.PULL_UP)
        self.__pinR.set_pull(self.__pinR.PULL_UP)

    def set_motors_speed(self, left_wheel_speed: int, right_wheel_speed: int):
        """
        设置左右轮电机速度
        :param left_wheel_speed:左轮速度-100～100
        :param right_wheel_speed: 右轮速度-100～100
        :return: none
        """
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
        """
        设置车头灯颜色
        :param light:选择车灯
        :param R:R通道颜色0-255
        :param G:G通道颜色0-255
        :param B:B通道颜色0-255
        :return:none
        """
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
        """
        返回当前巡线头状态
        :return:00 均在白色
                10 左黑右白
                01 左白右黑
                11 均在黑色
        """
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
        """基本描述

        选择伺服电机并且设置角度/速度

        Args:
            servo (number): 选择第几个舵机（伺服电机）1,2
            angle (number): 设置舵机角度 0~180
        """
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


def rgb_diods(mic_level):
    r = diod_light_rand()
    g = diod_light_rand()
    b = diod_light_rand()
    ct.set_car_light(left, r, g, b)
    ct.set_car_light(right, r, g, b)

    if (mic_level > 8):
        r = diod_light_rand()
        g = diod_light_rand()
        b = diod_light_rand()

    color_fill(np, (r, g, b), 0)
    color_fill(np, (r, g, b), 1)


def diods5x5(mic_level):
    for y in range(5):
        brightness = 0
        if y == 4:
            if mic_level == 1:
                brightness = 5
            elif mic_level > 1:
                brightness = 9
            else:
                brightness = 0
        if y == 3:
            if mic_level > 3:
                brightness = 9
            elif mic_level > 2:
                brightness = 5
            else:
                brightness = 0
        if y == 2:
            if mic_level > 6:
                brightness = 9
            elif mic_level > 4:
                brightness = 5
            else:
                brightness = 0
        if y == 1:
            if mic_level > 8:
                brightness = 9
            elif mic_level > 7:
                brightness = 5
            else:
                brightness = 0
        if y == 0:
            if mic_level > 12:
                brightness = 9
            elif mic_level > 9:
                brightness = 5
            else:
                brightness = 0

        for x in reversed(range(5)):
            display.set_pixel(x, y, brightness)


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
