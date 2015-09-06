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
import io
import socket
import threading
import logging
import time

RESOLUTION = (1280, 720)
VIDEO_LENGTH = 30
IMG_PREFIX = "picam_"
IMG_SUFFIX = ""


##
# @brief Saves pictures to files when triggered.
##
class CameraController:

    ##
    # @brief Constructor.
    ##
    def __init__(self, path, port):
        self._camera = picamera.PiCamera()
        self._camera.resolution = RESOLUTION
        self._camera.framerate = 30
        time.sleep(2)
        logging.debug('CameraController: ' + str(self.__dict__))
        
        # stream for capturing and recording
        self._stream = picamera.PiCameraCircularIO(self._camera, seconds=10)
        self._camera.start_recording(self._stream, format='h264')

        # network stream
        self._thread = threading.Thread(target=self.provide_network_stream, args=(port,self._camera,)).start()

        logging.debug('CameraController: started.')

    ##
    # @brief Destructor.
    ##
    def __del__(self):
        self._camera.stop_recording()
        self._camera.close()
	logging.debug('CameraController: exit.')

    ##
    # @brief Thread providing a network stream.
    # 
    # Only one client can connect simultaneously.
    ##
    def provide_network_stream(self, port, camera):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('0.0.0.0', port))
        serversocket.listen(0)

        camera.start_recording('/dev/null', format='h264', splitter_port=2, resize=(320, 240))
        logging.info('CameraController: network stream provided.')

        try:
            while True:
                logging.info('CameraController: await connection ...')

                # accept a single connection and make a file-like
                # object out of it; this is blocking!
                (clientsocket, address) = serversocket.accept()
                connection = clientsocket.makefile('wb')

                # network stream with lower resolution
                camera.split_recording(connection, splitter_port=2)

                logging.info('CameraController: client (%s) connected to video stream.' %(address,))
    
                # await disconnect from client side
                try:
                    data = clientsocket.recv(10)
                    if len(data) == 0:
                        logging.info('CameraController: client (%s) disconnected.' %(address,))
                    else:
                        logging.debug('CameraController: client sent data (%s).' %(data,))
                except Exception as e:
                    logging.error('CameraController: %s' %(e,))
                finally:
                    # cleanup client socket
                    camera.split_recording('/dev/null', splitter_port=2)
                    clientsocket.close()

        except Exception as e:
            logging.error('CameraController: %s.' %(e,))
            raise
        # finally:
        #     # cleanup server socket
        #     camera.stop_recording(splitter_port=2)
        #     serversocket.close()
        #     logging.debug('CameraController: cleanup network streaming.')


    ##
    # @brief Captures a single picture and saves it to the server.
    ##
    def capture(self):
        filename = IMG_PREFIX + time.strftime('%y-%m-%d_%H-%M-%S', time.localtime()) + IMG_SUFFIX + '.jpg'
        self._camera.capture(filename, use_video_port=True)
        logging.info('CameraController: captured image ' + filename + '.')

    ##
    # @brief Wait recording in percent of the circular stream.
    ##
    def wait(self, percent=0.5):
        self._camera.wait_recording(VIDEO_LENGTH*percent)

    ##
    # @brief Writes the stream to a video file (.h264).
    ##
    def write_video(self):
        logging.info('CameraController: writing video')
        # prevent the camera's background writing thread from changing
        # the stream while our own thread reads from it (as the stream
        # is a circular buffer, a write can remove information that is
        # about to be read) -> so lock!
        with stream.lock:
            # find the first header frame in the video
            for frame in stream.frames:
                if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                    stream.seek(frame.position)
                    break
            # write the rest of the stream to disk
            with io.open('motion.h264', 'wb') as output:
                output.write(stream.read())
