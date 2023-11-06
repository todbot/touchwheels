# touchwheel_badgedemo.py -- try out touchwheel on Supercon2023 badge in CircuitPython
# 5 Nov 2023 - @todbot / Tod Kurt
#  originally from github.com/todbot/HackadayVectorscopeHacks
#
import time, math
import board
import touchio

# touchwheel plugged into GND,GP26,GP27,GP28 on side of Supercon2023 badge
touch_pins = (board.GP26, board.GP27, board.GP28)

class TouchWheel():
    """Simple capacitive touchweel made from three captouch pads """
    def __init__(self,touch_pins, offset=-0.333/2):
        self.touchins = []
        self.offset = offset # physical design is rotated 1/2 a sector anti-clockwise
        for p in touch_pins:
            touchin = touchio.TouchIn(p)
            self.touchins.append(touchin)

    def pos(self):
        """
        Given three touchio.TouchIn pads, compute wheel position 0-1
        or return None if wheel is not pressed
        """
        a = self.touchins[0]
        b = self.touchins[1]
        c = self.touchins[2]

        # compute raw percentages
        a_pct = (a.raw_value - a.threshold) / a.threshold
        b_pct = (b.raw_value - b.threshold) / b.threshold
        c_pct = (c.raw_value - c.threshold) / c.threshold
        #print( "%+1.2f  %+1.2f  %+1.2f" % (a_pct, b_pct, c_pct), end="\t")

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
        return (pos + self.offset) % 1 if pos is not None else None


touchwheel = TouchWheel(touch_pins)

while True:
    pos = touchwheel.pos()
    if pos is not None:   # touched!
        print("touch_pos:", pos)
    else:
        print("no touch")
    time.sleep(0.05)
