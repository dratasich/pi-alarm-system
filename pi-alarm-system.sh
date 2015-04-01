#!/bin/sh
##
# @file
# @author Denise Ratasich
# @date 28.03.2015
##

DIR="$HOME/.pi-alarm-system"
LOG_DIR="log"
LOG_FILE_STREAM="stream.log"
LOG_FILE_ALARM="alarm-system.log"
PORT=1816

usage()
{
    echo "Usage: $0 [-l [-p PORT]]" 1>&2
    exit 1
}

# check arguments
flag_l=0
flag_p=0
port=PORT

# parse options
temp=$(getopt lp: "$@")

# error in parsing
if [ $? -ne 0 ] 
then 
    usage 
fi

# check options
while [ $# -gt 0 ]
do
    case "$1" in
	(-l) 
	    flag_l=1
	    echo "-l"
	    ;;
	(-p) 
	    if [ $flag_l -eq 0 ]
	    then
		echo "$0: error - option -p is only allowed when -l is set" 1>&2
		usage
	    else
		echo "-p $optarg"
		flag_p=1
		port=optarg
	    fi
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
$(mkdir -p "${DIR}/${LOG_DIR}")
echo "$0: directories for log-files created ($DIR$LOG_DIR)"

# provide lifestream
if [ $flag_l -eq 1 ]
then
    echo "$0: provide stream"
    raspivid -t 0 -o - -w 800 -h 600 | cvlc -v stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554}' :demux=h264 >> "$DIR/$LOG_DIR/$LOG_FILE_STREAM"
fi

# start video and image capture by motion sensor
echo "$0: start motion detection"