# touchweel0_demo0.py -- quick test of the "touchwheel0" board w/ a Neopixel ring
#  Uses a super dumb algorthim to calculate wheel position
# 2 Nov 2023 - @todbot / Tod Kurt
#

import time
import board
import touchio
import neopixel

num_leds = 12
leds = neopixel.NeoPixel(board.GP15, num_leds, brightness=0.1)
leds[0] = 0x005500  # quick blip to indicate which LED is "up"
time.sleep(0.5)
leds[0] = 0

touch_pins = (board.GP18, board.GP19, board.GP20)
touchins = []
for p in touch_pins:
    touchin = touchio.TouchIn(p)
    touchins.append(touchin)

def wheel_pos(a,b,c):
    """
    Given three touchio.TouchIn pads, compute wheel position 0-1
    or return None if wheel is not pressed
    """
    # compute raw percentages
    a_pct = (a.raw_value - a.threshold) / a.threshold
    b_pct = (b.raw_value - b.threshold) / b.threshold
    c_pct = (c.raw_value - c.threshold) / c.threshold
    #print( "%+1.2f  %+1.2f  %+1.2f" % (a_pct, b_pct, c_pct), end="\t")

    offset = -0.333/2  # physical design is rotated 1/2 a sector anti-clockwise

    pos = None
    # cases when finger is touching two pads
    if a_pct >= 0 and b_pct >= 0:  #
        pos = 0 + 0.333 * (b_pct / (a_pct + b_pct))
    elif b_pct >= 0 and c_pct >= 0:  #
        pos = 0.333 + 0.333 * (c_pct / (b_pct + c_pct))
    elif c_pct >= 0 and a_pct >= 0:  #
        pos = 0.666 + 0.333 * (a_pct / (c_pct + a_pct))
    # special cases when finger is just on a single pad.
    # these shouldn't be needed and create "deadzones" at these points
    # so surely there's a better solution
    elif a_pct > 0 and b_pct <= 0 and c_pct <= 0:
        pos = 0
    elif a_pct <= 0 and b_pct > 0 and c_pct <= 0:
        pos = 0.333
    elif a_pct <= 0 and b_pct <= 0 and c_pct > 0:
        pos = 0.666
    # wrap pos around the 0-1 circle if offset puts it outside that range
    return (pos + offset) % 1 if pos is not None else None

dim_by = 20

while True:
    leds[:] = [[max(i-dim_by,0) for i in l] for l in leds]  # fade leds

    pos = wheel_pos(*touchins)
    if pos is not None:
        print("pos:%.2f" % pos)
        n = int(pos * num_leds)
        leds[n] = 0xff00ff
    else:
        print("no touch")

    time.sleep(0.01)
