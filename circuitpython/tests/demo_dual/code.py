# touchweel0_demo_dual.py -- show two "touchwheel0" boards w/ Neopixel rings
#  uses "touchslider.py" library
# 10 Nov 2023 - @todbot / Tod Kurt
# 10 Apr 2024 - @todbot / Tod Kurt
#

import time
import board
import touchio
import neopixel
import rainbowio

from touchslider import TouchWheel

num_leds = 16
ledsA = neopixel.NeoPixel(board.GP17, num_leds, brightness=0.2)
ledsB = neopixel.NeoPixel(board.GP16, num_leds, brightness=0.2)

wheelA = TouchWheel( (board.GP18, board.GP19, board.GP20), offset=0.25)
wheelB = TouchWheel( (board.GP11, board.GP12, board.GP13), offset=0.25)

dim_by = 20

while True:
    # fade down all LEDS to give neat trails
    ledsA[:] = [[max(i-dim_by,0) for i in l] for l in ledsA]  # fade leds
    ledsB[:] = [[max(i-dim_by,0) for i in l] for l in ledsB]  # fade leds

    # get current wheel position if touched, else None
    posA = wheelA.pos()
    posB = wheelB.pos()
    
    #print(posA, posB)
    
    if posA is not None:  # touched
        nA = num_leds - 1 - int(posA * num_leds)
        ledsA[nA] = rainbowio.colorwheel(time.monotonic()*50)

    if posB is not None:  # touched
        nB = num_leds - 1 - int(posB * num_leds)
        ledsB[nB] = rainbowio.colorwheel(time.monotonic()*50)
        
    time.sleep(0.01)
