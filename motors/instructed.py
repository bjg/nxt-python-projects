# /usr/bin/env python

from nxt.locator import find_one_brick
from nxt.motor import *
from time import sleep
from threading import Thread
from sys import exit, stdout

try:
    brick = find_one_brick()
except Exception as e:
    exit(e)

try:
    motors = [Motor(brick, PORT_B), Motor(brick, PORT_C)]
except Exception as e:
    exit(e)

# This is based on the cnc.py example that comes bundled with nxt-python

instructions = (
    {
        'wait': 0, 'steps': (
            {'motor': 0, 'power': 25, 'degrees': 360},
            {'motor': 1, 'power': 25, 'degrees': 360}
        )
    },
    {
        'wait': 1, 'steps': (
            {'motor': 0, 'power': 0, 'degrees': 0},
            {'motor': 1, 'power': 25, 'degrees': 360}
        )
    }
)
ts = []


def turn_motor(motor, power, degrees):
    try:
        motor.turn(power, degrees)
    except Exception as e:
        stdout.write(e)


def execute(s):
    t = Thread(target=turn_motor, args=(motors[s['motor']], s['power'], s['degrees']))
    t.deamon = True
    ts.append(t)
    t.start()


for inst in instructions:
    for step in inst['steps']:
        sleep(inst['wait'])
        execute(step)

for t in ts:
    t.join()
