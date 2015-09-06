#!/usr/bin/python
##
# @file
# @author Denise Ratasich
# @date 22.03.2015
#
# @brief Captures images, records video when the motion sensor
# triggers and provides a network stream for online surveillance.
##

import logging
import sys
import time
import argparse
import gpio
from camera import CameraController

# default settings
PIN_MOTION_SENSOR = 15  ## pin from the motion sensor near the camera (directly)
PIN_ALARM = 16          ## additional pin from the alarm system switch
STREAM_PORT = 8000      ## port where network stream of camera is provided

# parse arguments for individual settings
argparser = argparse.ArgumentParser()
group = argparser.add_mutually_exclusive_group(required=True)
group.add_argument('-m', '--motion_pin', type=int, help='GPIO pin number (board) where motion sensor is connected to trigger capturing and recording. Check valid pins at http://pi.gadgetoid.com/pinout.')
group.add_argument('-a', '--alarm_pin', type=int, help='GPIO pin number (board) where alarm system is connected to trigger capturing and recording. Check valid pins at http://pi.gadgetoid.com/pinout.')
argparser.add_argument('-p', '--port', type=int, help='Port where network stream of camera should be provided.')
args = argparser.parse_args()

if args.motion_pin is not None:
    PIN_MOTION_SENSOR = args.motion_pin
if args.alarm_pin is not None:
    PIN_ALARM = args.alarm_pin
if args.port is not None:
    STREAM_PORT = 8000

# will be initialized (main)
alarm = False

##
# @brief Called when the motion sensor triggers.
##
def callback_motion_sensor():
    global alarm # alarm should be interpreted as global variable
    if not alarm:
        logging.info('Motion sensor: detection!')
        alarm = True

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
    logging.info('Make sure the motion sensor is connected to GPIO pin ' + str(PIN_MOTION_SENSOR) + '.')

    # init camera
    cam = CameraController(path='.', port=STREAM_PORT)

    # do the stuff to do
    while True:
        if alarm:
            cam.capture() # make/save single image
            cam.wait(0.5) # wait 50% of video length
            cam.write_video()
            logging.info('Capturing done.')

except RuntimeWarning as e:
    logging.warn(e)
except KeyboardInterrupt:
    logging.info('Exit by user.')
except Exception as e:
    logging.error(e)
    raise
except:
    logging.error('Unexpected error.')
    raise

# cleanup
del motion_sensor
del cam
