#!/usr/bin/python
"""@file

"""

import motion_sensor

def callback():
    print 'test'

motion_sensor = MotionSensor(5, callback)
motion_sensor.start()
