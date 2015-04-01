#!/usr/bin/python
##
# @file
# @author Denise Ratasich
# @date 22.03.2015
#
# @brief Captures images and records videos when the motion sensor
# triggers.
##

import logging
import sys
import time
import gpio
from camera import CameraController

PIN_MOTION_SENSOR = 15  # pin from the motion sensor near the camera (directly)
PIN_ALARM = 16          # additional pin from the alarm system switch

# will be initialized (main)
motion_sensor = None
cam = None

##
# @brief Called when the motion sensor triggers.
##
def callback_motion_sensor():
    logging.info('Motion sensor: detection!')
#    cam.capture()
    cam.record()

##
# @brief Start of the program.
##

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
    # init motion sensor
    motion_sensor = gpio.EdgeMonitor(PIN_MOTION_SENSOR, gpio.FALLING, callback_motion_sensor)
    motion_sensor.start()
    logging.info('Make sure the motion sensor is connected to GPIO pin ' + 
		 str(PIN_MOTION_SENSOR) + '.')

    # init camera
    cam = CameraController()

    # wait recording
    while True:
        cam.work()

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
