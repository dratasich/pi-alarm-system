"""@file

The motion sensor connected to a general purpose input is periodically
checked. When the motion sensor's input turns 0? the camera module is
triggered to record the camera frames.

"""

import RPi.GPIO as gpio
import logging

"""Invokes callback function if motion sensor triggers."""
class MotionSensor:

    """Constructor."""
    def __init__(self, gpio_pin, callback):
	"""init attributes"""
        self._gpio_pin = gpio_pin
        self.setcallback(callback)

	"""set pin connected to motion sensor as input"""
	gpio.setmode(gpio.BOARD)
	gpio.setup(self._gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

	logging.debug('MotionSensor: ' + str(self.__dict__))

    """Pass function that should be called when motion sensor triggers."""
    def setcallback(self, fct):
        if callable(fct):
            self._callback = fct
            logging.debug('MotionSensor: ' + str(fct) + ' will be called when edge detected.')
        else:
            raise Exception('MotionSensor: The passed parameter is not callable!')

    def gpio_callback(self, gpio_pin):
	logging.debug('MotionSensor: edge detected.')
        self._callback()

    """Periodically check the motion sensor."""
    def start(self):
	gpio.add_event_detect(self._gpio_pin, gpio.FALLING, callback=self.gpio_callback)
        logging.info('MotionSensor: started.')
