##
# @file
# @author Denise Ratasich
# @date 24.03.2015
#
# @brief Controls the pi camera.
#
# This module collects functions to control the pi camera. It is
# slightly adapted from
# http://picamera.readthedocs.org/en/release-1.10/recipes2.html.
##

import picamera
import picamera.array
import io
import socket
import threading
import logging
import time
import numpy as np

RESOLUTION = (1280, 720)
VIDEO_LENGTH = 20
IMG_PREFIX = "picam_"
IMG_SUFFIX = ""
VID_PREFIX = "picam_"
VID_SUFFIX = ""


##
# @brief Saves pictures to files when triggered.
##
class CameraController:

    ##
    # @brief Constructor.
    ##
    def __init__(self, path, motion_callback=None):
        self._camera = picamera.PiCamera()
        self._camera.resolution = RESOLUTION
        self._camera.framerate = 30
        time.sleep(2)
        logging.debug('CameraController: ' + str(self.__dict__))

        # save path where videos and images should be logged
        self._path = path
        logging.info('CameraController: videos/images will be saved to ' + path)

        # motion detection with camera
        if motion_callback is None:
            self._motion_output = None
        else:
            self._motion_output = MotionDetector(self._camera, motion_callback)

        # stream for capturing and recording
        self._stream = picamera.PiCameraCircularIO(self._camera,
                                                   seconds=VIDEO_LENGTH)
        self._camera.start_recording(self._stream, format='h264',
                                     motion_output=self._motion_output)

        logging.debug('CameraController: started.')

    ##
    # @brief Destructor.
    ##
    def __del__(self):
        self._camera.stop_recording()
        self._camera.close()
	logging.debug('CameraController: exit.')

    ##
    # @brief Captures a single picture and saves it to the server.
    ##
    def capture(self, filename=None):
        if filename is None:
            filename = self._path + IMG_PREFIX + time.strftime('%y-%m-%d_%H-%M-%S', time.localtime()) + IMG_SUFFIX + '.jpg'
        self._camera.capture(filename, use_video_port=True)
        logging.debug('CameraController: captured image ' + filename + '.')

    ##
    # @brief Wait recording in percent of the circular stream.
    ##
    def wait(self, percent=0.5):
        self._camera.wait_recording(VIDEO_LENGTH*percent)

    ##
    # @brief Writes the stream to a video file (.h264).
    ##
    def write_video(self, filename=None):
        if filename is None:
            filename = self._path + VID_PREFIX + time.strftime('%y-%m-%d_%H-%M-%S', time.localtime()) + VID_SUFFIX + '.h264'
        # prevent the camera's background writing thread from changing
        # the stream while our own thread reads from it (as the stream
        # is a circular buffer, a write can remove information that is
        # about to be read) -> so lock!
        with self._stream.lock:
            # find the first header frame in the video
            for frame in self._stream.frames:
                if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                    self._stream.seek(frame.position)
                    break
            # write the rest of the stream to disk
            with io.open(filename, 'wb') as output:
                output.write(self._stream.read())
        logging.debug('CameraController: wrote video ' + filename + '.')


# http://picamera.readthedocs.io/en/release-1.12/recipes2.html#custom-outputs
class MotionDetector(picamera.array.PiMotionAnalysis):
        
    def __init__(self, camera, motion_callback):
        super(MotionDetector, self).__init__(camera)
        self._callback = motion_callback

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10:
            logging.debug('MotionDetector: motion detected!')
            self._callback()
