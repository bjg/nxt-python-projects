#/usr/bin/env python

from nxt.locator import find_one_brick
from nxt.motor import *
import threading, sys


def turn_motor(m, power, degrees):
    try:
        m.turn(power, degrees)
    except Exception as e:
        sys.stdout.write(e)

brick = find_one_brick()
right, left = Motor(brick, PORT_B), Motor(brick, PORT_C)

ts = []
for motor in [left, right]:
    t = threading.Thread(target=turn_motor, args=(motor, 75, 3600))
    t.deamon = True
    ts.append(t)

for t in ts:
    t.start()

for t in ts:
    t.join()
