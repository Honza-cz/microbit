# Imports go at the top
from microbit import *
import neopixel
import random
import time
import log
import math

main_colors = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
    (0, 255, 255), # Cyan
    (255, 0, 255), # Magenta
    # (255, 255, 255), # White
    # (0, 0, 0),     # Black
    # (128, 128, 128), # Gray
    # (100, 100, 100), # Dark Gray
    # (200, 200, 200), # Light Gray
    (0, 0, 100),    # Dark Blue
    (0, 150, 200),  # Light Blue
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
    (255, 192, 203) # Pink
]

def blink(np, context, burn_period, dark_period):

    color_picker = lambda x: main_colors[x % len(main_colors)]

    if not context:
        context = (0, dark_period, True, 0)

    last_time_tick, delay, burn, color_index = context
    current_time_ms = time.ticks_ms()

    if (last_time_tick == 0 or current_time_ms>last_time_tick+delay):
        last_time_tick=current_time_ms

        color = (0,0,0)
        if burn: 
                color = color_picker(color_index)
                color_index += 1

        for i in range(len(np)):
            if burn: 
                np[i] = color
            else:
                np[i] = color
                
            
        np.show()
        burn = not burn

    return (last_time_tick, dark_period if burn else burn_period, burn, color_index)

def light_on_from_edge_to_middle(context):
    if not context:
        context = (True, 0)
    burn, last_time_tick = context

    current_time_ms = time.ticks_ms()

    images = [Image.HEART,Image.HEART_SMALL,Image.HAPPY,Image.SMILE,Image.SAD,Image.CONFUSED,Image.ANGRY,Image.ASLEEP,Image.SURPRISED,Image.SILLY,Image.FABULOUS,Image.MEH,Image.YES,Image.NO,Image.CLOCK12, Image.CLOCK11, Image.CLOCK10, Image.CLOCK9, Image.CLOCK8, Image.CLOCK7, Image.CLOCK6, Image.CLOCK5, Image.CLOCK4, Image.CLOCK3, Image.CLOCK2, Image.CLOCK1,Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE, Image.ARROW_S, Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW,Image.TRIANGLE,Image.TRIANGLE_LEFT,Image.CHESSBOARD,Image.DIAMOND,Image.DIAMOND_SMALL,Image.SQUARE,Image.SQUARE_SMALL,Image.RABBIT,Image.COW,Image.MUSIC_CROTCHET,Image.MUSIC_QUAVER,Image.MUSIC_QUAVERS,Image.PITCHFORK,Image.XMAS,Image.PACMAN,Image.TARGET,Image.TSHIRT,Image.ROLLERSKATE,Image.DUCK,Image.HOUSE,Image.TORTOISE,Image.BUTTERFLY,Image.STICKFIGURE,Image.GHOST,Image.SWORD,Image.GIRAFFE,Image.SKULL,Image.UMBRELLA,Image.SNAKE,Image.SCISSORS]

    if last_time_tick == 0 or current_time_ms > (last_time_tick + (800)):
        last_time_tick=current_time_ms
        if burn:
            display.show(Image('99999:'
                            '99999:'
                            '99999:'
                            '99999:'
                            '99999'))
        else:
            display.show(random.choice(images))
        burn = not burn

    return (burn, last_time_tick)


def main():
    np = neopixel.NeoPixel(pin1, 6)
    np.clear()
    np.show()


    context = None
    contextLedPanel = None
    last_switched = time.ticks_ms()
    index = 0

    all_effects = [  
        lambda ctx: blink(np,ctx, 400, 1000),        
        lambda ctx: blink(np,ctx, 1000, 400),        
    ]

    all_effects_led_pannel = [
        lambda ctx: light_on_from_edge_to_middle(ctx)
    ]

    while(True):

        if (last_switched + 20000) < time.ticks_ms():

            sleep(100)
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