# pi-alarm-system

## Surveillance Camera

Start alarm_system.py to capture images when motion is detected (via
external motion sensor connected to a GPIO pin). Video is recorded in
a circular buffer and saved too when motion is detected. Furthermore a
network stream (mjpg) is provided on port 8080.

### TODOs

- [X] read from GPIO if motion sensor detects a movement
- [X] trigger picamera to record a picture and video when motion is
      detected
- [X] provide interface for live stream (via mjpg streamer)
- [ ] capture images for mjpg streamer


## Network stream only

A network stream can be provided with (here 1816 is the port number):
  	  raspivid -t 0 -o - -w 800 -h 600 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:1816}' :demux=h264

With VLC player it is then accessible over a network stream with
address: 'rtsp://192.168.1.45:1618/'.


## Settings

- Do not forget to enable the camera (e.g., with sudo raspi-config).
- To disable the LED on the camera PCB when recording, turn it off by
  adding following line to /boot/config.txt (will get active after
  reboot: 
  	  disable_camera_led=1


## References

- picamera Package API Documentation: http://picamera.readthedocs.org
- RPi.GPIO Package API Documentation: http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
- mjpg-streamer Installation: http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi
