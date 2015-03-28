##
# @file
# @author Denise Ratasich
# @date 24.03.2015
#
# @brief Controls the pi camera.
#
# This module collects functions to control the pi camera.
##

import picamera
import logging
import time

RESOLUTION = (1280, 720)
VIDEO_LENGTH = 20
IMG_PREFIX = "picam_"
IMG_SUFFIX = ""

##
# @brief Saves pictures to files when triggered.
##
class CameraController:

    ##
    # @brief Constructor.
    ##
    def __init__(self):
        self._camera = picamera.PiCamera()
        self._camera.resolution = RESOLUTION
        self._stream_circular = picamera.PiCameraCircularIO(self._camera, VIDEO_LENGTH)
        logging.debug('CameraController: ' + str(self.__dict__))
        
        # make ready
        self._camera.start_preview()
        time.sleep(2)
        logging.debug('CameraController: started.')

    def __exit__(self):
        self._camera.close()
	logging.debug('CameraController: exit.')

    ##
    # @brief Captures a single picture and saves it to the server.
    ##
    def capture(self):
        filename = IMG_PREFIX + time.strftime('%y-%m-%d_%H-%M-%S', time.localtime()) + IMG_SUFFIX + '.jpg'
        self._camera.capture(filename)

    ##
    # @brief Record
    ##
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
