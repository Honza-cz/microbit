# Imports go at the top
from microbit import *
import neopixel
import random
import time

main_colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128),
               (0, 255, 255), (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128)]


def basic(np, context, main_colors):
    if not context:
        it = iter(main_colors)
        c = next(it)
        context = (it, True, 0, 0, c)

    color_iterator, regular, last_time_tick, diod_index, color = context

    current_time_ms = time.ticks_ms()
    next_diod_index = diod_index
    if current_time_ms > (last_time_tick + 100):
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
    if current_time_ms > (last_time_tick + 2):
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


def glow_colored(np, context):
    if not context:
        context = (True, 0, 0, (0, 0, 0), (255, 0, 0), 10)

    regular, last_time_tick, rgb_index, rgb, rgb_max, wait_time = context
    r, g, b = rgb

    current_time_ms = time.ticks_ms()
    if current_time_ms > (last_time_tick + wait_time):
        for diod_index in range(6):
            if rgb_index == 0:
                np[diod_index] = rgb
            elif rgb_index == 1:
                np[diod_index] = rgb
            elif rgb_index == 2:
                np[diod_index] = rgb

        np.show()
        c = r
        if (rgb_index == 0):
            c = r
        elif (rgb_index == 1):
            c = g
        else:
            c = b
        wait_time = 10
        if regular:
            if c + 1 <= 255:
                c += 1
                r, g, b = increment_till_max(rgb, rgb_max)

            else:
                regular = not regular
                wait_time = 1000
                c -= 1
                r, g, b = decrement_till_min(rgb, (0, 0, 0))
        else:
            if c - 1 >= 0:
                c -= 1
                r, g, b = decrement_till_min(rgb, (0, 0, 0))
            else:
                regular = not regular
                c = 1
                r, g, b = increment_till_max(rgb, rgb_max)
                if (rgb_index + 1) < 2:
                    rgb_index += 1
                else:
                    rgb_index = 0
                    all_indexes = [0, 1, 2]
                    del all_indexes[rgb_index]

                    rnd_color_index = random.choice(all_indexes)
                    if (rnd_color_index == 0):
                        rgb_max = (random.randint(0, 255), 0, 0)
                    elif (rnd_color_index == 1):
                        rgb_max = (0, random.randint(0, 255), 0)
                    else:
                        rgb_max = (0, 0, random.randint(0, 255))
        if (rgb_index == 0):
            r = c
        elif (rgb_index == 1):
            g = c
        else:
            b = c

        last_time_tick = current_time_ms

    return (regular, last_time_tick, rgb_index, (r, g, b), rgb_max, wait_time)


def increment_till_max(rgb, rgb_max):
    r = (rgb[0] + 1) if (rgb[0] + 1) <= rgb_max[0] else rgb[0]
    g = (rgb[1] + 1) if (rgb[1] + 1) <= rgb_max[1] else rgb[1]
    b = (rgb[2] + 1) if (rgb[2] + 1) <= rgb_max[2] else rgb[2]
    return (r, g, b)


def decrement_till_min(rgb, rgb_min):
    r = (rgb[0] - 1) if (rgb[0] - 1) >= rgb_min[0] else rgb[0]
    g = (rgb[1] - 1) if (rgb[1] - 1) >= rgb_min[1] else rgb[1]
    b = (rgb[2] - 1) if (rgb[2] - 1) >= rgb_min[2] else rgb[2]
    return (r, g, b)


def rocket_explosion(np, context, colors):
    if not context:
        context = (0, 0, random.choice(colors), False)

    index, last_time_tick, color, burn_mode = context

    current_time_ms = time.ticks_ms()

    if burn_mode:
        last_time_tick = current_time_ms
        for i in range(6):
            np[i] = color
        burn_mode = False
    elif current_time_ms > (last_time_tick + 500):
        last_time_tick = current_time_ms
        for i in range(6):
            np[i] = (0, 0, 0)

        if index == 0:
            color = random.choice(colors)
            np[index] = color
        elif index < len(np):
            np[index] = color
        else:
            burn_mode = True

        index += 1
        index %= 7

    np.show()

    return (index, last_time_tick, color, burn_mode)


def light_on_one_by_one(context):
    if not context:
        context = (0, 0, 9, 0)
    x, y, l, last_time_tick = context

    current_time_ms = time.ticks_ms()

    if current_time_ms > (last_time_tick + (10 * x * y + 20)):

        display.set_pixel(x, y, l)
        x += 1
        if (x > 4):
            x = 0
            y += 1
            if (y > 4):
                y = 0
                if l == 0:
                    l = 9
                else:
                    l = 0
        return (x, y, l, current_time_ms)
    return context


def light_on_from_edge_to_middle(context):
    if not context:
        context = (0, 0, 9, 0)
    x, y, l, last_time_tick = context

    current_time_ms = time.ticks_ms()

    if current_time_ms > (last_time_tick + (100)):
        led_count = 5 - 1

        display.set_pixel(x, y, l)
        display.set_pixel(-x + led_count, y, l)
        if y == led_count and x == led_count:
            if l == 0:
                l = 9
            elif l == 9:
                l = 0
            return (0, 0, l, current_time_ms)
        if (x == led_count):
            return (0, y + 1, l, current_time_ms)
        else:
            return (x + 1, y, l, current_time_ms)
    return context


def main():
    np = neopixel.NeoPixel(pin1, 6)
    np.clear()
    np.show()

    context = None
    contextLedPanel = None
    last_switched = time.ticks_ms()
    index = 0

    all_effects = [
        lambda ctx: rocket_explosion(np, ctx, main_colors),
        lambda ctx: glow(np, ctx),
        lambda ctx: glow_colored(np, ctx),
        lambda ctx: basic(np, ctx, main_colors + [(0, 0, 0)])
    ]

    all_effects_led_pannel = [
        lambda ctx: light_on_one_by_one(ctx),
        lambda ctx: light_on_from_edge_to_middle(ctx)
    ]

    while(True):

        if (last_switched + 30000) < time.ticks_ms():

            sleep(200)
            context = None
            contextLedPanel = None
            index += 1
            last_switched = time.ticks_ms()
            display.clear()

        context = all_effects[index % len(all_effects)](context)
        contextLedPanel = all_effects_led_pannel[index % len(all_effects_led_pannel)](contextLedPanel)


if __name__ == '__main__':
    main()
    display.show(Image.HEART)
