"""@file

@brief Controls the pi camera.
@author Denise Ratasich
@date 24.03.2015

This module collects functions to control the pi camera.

"""

import picamera
import logging
import time

RESOLUTION = (1280, 720)
VIDEO_LENGTH = 20

"""Saves pictures to files when triggered."""
class PictureSaver:

    """Constructor."""
    def __init__(self):
        self._camera = picamera.PiCamera()
        self._camera.resolution = RESOLUTION
        self._stream_circular = picamera.PiCameraCircularIO(self._camera, VIDEO_LENGTH)
        logging.debug('PictureSaver: ' + str(self.__dict__))
        
        # make ready
        self._camera.start_preview()
        time.sleep(2)
        self._camera.start_recording()
        logging.debug('PictureSaver: started.')

    def __exit__(self):
        self._camera.close()
	logging.debug('PictureSaver: exit.')

    """Captures a single picture and saves it to the server."""
    def capture(self):
        filename = strftime('%y-%m-%d_%H-%M-%S', localtime()) + '_picam.jpg'
        self._camera.capture(filename)

    """Record"""
    def record():
        logging.debug('Writing video.')
        stream = self._stream_circular
        with stream.lock:
            # find the first header frame in the video
            for frame in stream.frames:
                if frame.frame_type == self._camera.PiVideoFrameType.sps_header:
                    stream.seek(frame.position)
                    break
            # write the rest of the stream to disk
            with io.open('motion.h264', 'wb') as output:
                output.write(stream.read())
