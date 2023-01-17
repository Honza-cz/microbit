from microbit import *
from time import sleep_us
from machine import time_pulse_us
import random

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


distances = []
if __name__ == '__main__':
    ct = CUTEBOT()

    display.show("R")
    sleep(5000)

    # while True:
    # display.scroll(ct.get_distance())
    # display.scroll('-')

    for i in range(50):
        ct.set_motors_speed(-20, 20)
        sleep(100)
        ct.set_motors_speed(0, 0)

        added = False
        for i in range(5):
            sleep(100)
            d = ct.get_distance()
            if d != 0:
                distances.append(d)
                added = True
                break
        if not added:
            distances.append(0)

    ct.set_motors_speed(0, 0)
    display.scroll('MD')
    if 0 in distances:
        max_distance = 0
    else:
        max_distance = max(distances)
    display.scroll(max_distance)
    while True:
        ct.set_motors_speed(-20, 20)
        sleep(100)
        ct.set_motors_speed(0, 0)
        curr_distance = 0
        for i in range(5):
            sleep(100)
            curr_distance = ct.get_distance()
            if curr_distance != 0:
                break

        if max_distance == 0 and curr_distance == 0:
            display.scroll("Done")
            display.scroll(curr_distance)
            sleep(5000)
            break
        elif curr_distance >= max_distance - 10:
            display.scroll("Done")
            display.scroll(curr_distance)
            sleep(5000)
            break

    # display.show("D")
    ct.set_motors_speed(0, 0)
    # sleep(1000)
