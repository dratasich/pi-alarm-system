# pi-alarm-system


## Surveillance Camera

Start `pi-alarm-system.py` to capture images when motion is detected
(via external motion sensor connected to a GPIO pin, or via camera,
see options of `alarm_system.py`).

On motion detection: captures and saves an image to the specified
folder, records and saves a video (circular buffer).

The start-up script `pi-alarm-system.py -l` provides a network stream
(mjpg-streamer) on port 8080.

### TODOs

- [ ] mount server and save data to server or install syncthing


## Network stream only

A network stream can be provided with (here 1816 is the port number):
```bash
raspivid -t 0 -o - -w 800 -h 600 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:1816}' :demux=h264
```

With VLC player it is then accessible over a network stream with
address: `rtsp://192.168.1.45:1618/`.


## Settings

- Do not forget to enable the camera (e.g., with sudo raspi-config).
- To disable the LED on the camera PCB when recording, turn it off by
  adding following line to /boot/config.txt (will get active after
  reboot:
  ``` 
  disable_camera_led=1
  ```
- Setup crontab for start-up script:
  ```
  $ sudo crontab -e
  # ...
  @reboot /path-to-script/pi-alarm-system.sh -l
  ```
- Install mjpg-streamer if you want to provide a live stream.
- If you want to access the [homepage](www-info/README.md) or the live
  stream, you will need to install `apache2`.


## References

- [picamera Package API Documentation](http://picamera.readthedocs.org)
- [RPi.GPIO Package API Documentation](http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
- [mjpg-streamer Installation](http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi)
- [Raspberry Pi Web Server](https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md)
