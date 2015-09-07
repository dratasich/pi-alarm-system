#!/bin/sh
##
# @file
# @author Denise Ratasich
# @date 28.03.2015
##

DIR="$HOME/.pi-alarm-system"
STREAM_DIR="stream"
REC_DIR="recordings"
LOG_DIR="log"
LOG_FILE_STREAM="mjpg_streamer.log"
LOG_FILE_ALARM="alarm_system.log"

# print usage and exit
usage()
{
    echo "Usage: $0 [-l]" 1>&2
    echo "  -l       Activate lifestream." 1>&2
    echo "           The lifestream is accessible through 'http://<IP of RaspberryPI>:8080/' (e.g., browser, VLC media player)" 1>&2
    exit 1
}

# kill running instances
killall mjpg_streamer > /dev/null 2>&1
if [ $? -eq 0 ]
then
    echo "$0: killed running mjpg_streamer processes"
fi
sudo killall alarm_system.py > /dev/null 2>&1
if [ $? -eq 0 ]
then
    echo "$0: killed running alarm_system processes"
fi

# check arguments
flag_l=0

# parse options
temp=$(getopt hl "$@")

# error in parsing
if [ $? -ne 0 ]
then
    usage
fi

# check options
while [ $# -gt 0 ]
do
    case "$1" in
	(-h)
	    usage
	    ;;
	(-l)
	    flag_l=1
	    ;;
	(--)
	    shift
	    break
	    ;;
	(-*)
	    echo "$0: error - unrecognized option $1" 1>&2
	    usage
	    ;;
	(*)
	    break
	    ;;
    esac
    shift
done


# make log dir if it does not exist (-p)
mkdir -p "${DIR}/${LOG_DIR}"
echo "$0: directory for log-files created: ${DIR}/${LOG_DIR}/"

# provide lifestream
if [ $flag_l -eq 1 ]
then
    # make stream dir if it does not exist (-p)
    mkdir -p "${DIR}/${STREAM_DIR}"
    echo "$0: directory for stream created: ${DIR}/${STREAM_DIR}/"

    # start mjpg-streamer (uses pic.jpg in stream directory as input)
    LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f ${DIR}/${STREAM_DIR} -n pic.jpg" -o "output_http.so -w ./www" > "${DIR}/${LOG_DIR}/${LOG_FILE_STREAM}" 2>&1 &
fi

# make log dir for images/videos if it does not exist (-p)
mkdir -p "${DIR}/${REC_DIR}"
echo "$0: directory for log-files created: ${DIR}/${REC_DIR}/"

# start video and image capture by motion sensor
echo "$0: start motion detection"
sudo ./src/alarm_system.py -m 15 --recordings "${DIR}/${REC_DIR}/" --stream "${DIR}/${STREAM_DIR}/pic.jpg" > "${DIR}/${LOG_DIR}/${LOG_FILE_ALARM}" 2>&1 &
