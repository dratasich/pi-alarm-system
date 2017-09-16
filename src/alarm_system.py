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

##
# @brief Start of the program.
##

# parse arguments for individual settings
argparser = argparse.ArgumentParser()
group = argparser.add_mutually_exclusive_group(required=False)
group.add_argument('-m', '--motion_pin', type=int,
                   help="""GPIO pin number (board) where motion sensor
                   is connected to trigger capturing and
                   recording. Check valid pins at
                   http://pi.gadgetoid.com/pinout.""")
group.add_argument('-a', '--alarm_pin', type=int,
                   help="""GPIO pin number (board) where alarm system
                   is connected to trigger capturing and
                   recording. Check valid pins at
                   http://pi.gadgetoid.com/pinout.""")
argparser.add_argument('-c', '--camera_motion', action='store_true',
                       help="""Perform motion detection with camera.""")
argparser.add_argument('--recordings', required=True,
                       help="""Path to the directory where the
                       images/videos should be saved when motion is
                       detected.""")
argparser.add_argument('--stream', required=True,
                       help="""Path to the picture that is used by the
                       mjpg streamer.""")
args = argparser.parse_args()

if args.motion_pin is not None:
    PIN_MOTION_SENSOR = args.motion_pin
if args.alarm_pin is not None:
    PIN_ALARM = args.alarm_pin

# set logging settings
root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)5s]: %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

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
# @brief Called when motion is detected in subsequent camera images.
##
def callback_motion_camera():
    global alarm
    if not alarm:
        logging.info('Camera: motion detection!')
        alarm = True

# main
try:
    # init motion sensor
    motion_sensor = gpio.EdgeMonitor(PIN_MOTION_SENSOR, gpio.FALLING, callback_motion_sensor)
    motion_sensor.start()
    logging.info('Make sure the motion sensor is connected to GPIO pin ' + str(PIN_MOTION_SENSOR) + '.')

    # init camera
    cam = CameraController(path=args.recordings,
                           motion_callback=callback_motion_camera)

    # do the stuff to do
    while True:
        # save image for mjpg-streamer
        cam.capture(args.stream)
        # save video and image to server if motion detected
        if alarm:
            cam.capture() # make/save single image
            cam.wait(0.5) # wait 50% of video length
            cam.write_video()
            logging.info('Capturing done.')
            alarm = False

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
