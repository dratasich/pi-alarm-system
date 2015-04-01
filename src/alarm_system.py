#!/usr/bin/python
##
# @file
# @author Denise Ratasich
# @date 22.03.2015
##

import logging
import sys
import time
import gpio
from camera import CameraController

PIN_MOTION_SENSOR = 15  # pin from the motion sensor near the camera (directly)
PIN_ALARM = 16          # additional pin from the alarm system switch

def callback_motion_sensor():
    print 'Motion sensor: detection!'

# set logging settings
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)5s]: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

# main
try:
    # test motion sensor
    motion_sensor = gpio.EdgeMonitor(PIN_MOTION_SENSOR, gpio.FALLING, callback_motion_sensor)
    motion_sensor.start()
    logging.info('Make sure the motion sensor is connected to GPIO pin ' + 
		 str(PIN_MOTION_SENSOR) + '.')

    #cam = CameraController()
    #cam.capture()

    while True:
        time.sleep(3600)        # sleep for an hour or so

except RuntimeWarning as e:
    logging.warn(e)
except KeyboardInterrupt:
    logging.info('exit by user')
except Exception as e:
    logging.error(e)
    raise
except:
    logging.error('Unexpected error.')
    raise
