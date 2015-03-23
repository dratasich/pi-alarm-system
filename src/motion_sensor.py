"""@file

The motion sensor connected to a general purpose input is periodically
checked. When the motion sensor's input turns 0? the camera module is
triggered to record the camera frames.

"""

import RPi.GPIO as GPIO
import logging

"""GPIO ID where the motion sensor is connected to."""
GPIO_ID_MOTION_SENSOR = 10

"""Invokes callback function if motion sensor triggers."""
class MotionSensor:

    """Constructor."""
    def __init__(self, gpio_id=GPIO_ID_MOTION_SENSOR, callback=None):
        self._gpio_id = gpio_id
        self._callback = callback
        logging.info('MotionSensor: initialized with GPIO ID = ' +
                     str(self._gpio_id) + ' and callback = ' +
                     str(self._callback) + '.')

    """Pass function that should be called when motion sensor triggers."""
    def setcallback(self, fct):
        if callable(fct):
            self._callback = fct
            logging.info('MotionSensor: callback function set to ' + str(fct) + '.')
        else:
            raise Exception('MotionSensor: The passed parameter is not callable!')

    def gpio_callback(self, gpio_id, value):
        self._callback()

    """Periodically check the motion sensor."""
    def start(self):
        """register interrupt"""
        GPIO.add_interrupt_callback(self._gpio_id, self.gpio_callback,
                                    edge='falling',
                                    threaded_callback=False)
        logging.info('MotionSensor: GPIO interrupt registered.')
        GPIO.wait_for_interrupts(threaded=True)
        logging.info('MotionSensor: started.')
