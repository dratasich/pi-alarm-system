# pi-alarm-system

A network stream can be provided with:
  	  raspivid -t 0 -o - -w 800 -h 600 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264


## Settings

- Do not forget to enable the camera (e.g., with sudo raspi-config).
- To disable the LED on the camera PCB when recording, turn it off by
  adding following line to /boot/config.txt (will get active after
  reboot: 
  	  disable_camera_led=1


## TODOs
- [ ] read from GPIO if motion sensor detects a movement
- [ ] trigger picamera to record some seconds of video
- [ ] provide web interface for live pictures


## References

- picamera Package API Documentation: http://picamera.readthedocs.org
- RPi.GPIO Package API Documentation: http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
