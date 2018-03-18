#!/bin/bash

# A script to automatically check if a phone is connected and record a video each time it is connected

# Removing previous error.txts when starting the script
if [ -f /home/shoban/error.txt ]
then
    sudo rm /home/shoban/error.txt
fi
    
# Function to check if a device is connected
function isconnected(){
    if ! [ -f /home/shoban/error.txt ] 
    then
        echo "No error.txt - Starting FFMPEG"
        return 0
    else
	if grep -Eq "Last message repeated|No medium found|Dequeued v4l2 buffer contains corrupted data" error.txt
	then
    	    echo "No device connected"
    	    pid=`pidof ffmpeg`
            sudo kill -9 $pid
   	    sudo rm error.txt
            return 0
        else
            echo "Device connected"
            return 1
	fi
    fi
}
 
# Main function to continuosly check if a device in connection and record video
while [ 1 ]
do
# To note the current date and time to name the recorded output
now="$(date +%s)"
isconnected
a=$?
#echo $a
# To check if a device is already connected and recording, if not try starting the recording
if [[ $a -eq 0 ]] 
then
    echo "FFMEPG Started"
    # Records the frame grabbed from the phone at the rate of 10 fps - suitable for good resolution
    ffmpeg -framerate 10 -analyzeduration 2 -f v4l2 -i /dev/video1 /home/shoban/Project/Videos/output_$now.mkv >& error.txt & 
else
    echo "Yes device connected"
fi
# ffmpeg -probesize 32 -framerate 25 -analyzeduration 2 -f v4l2 -t 00:00:05 -i /dev/video1 output_$now.mkv 
#ffmpeg -probesize 32 -framerate 25 -analyzeduration 2 -f v4l2 -i /dev/video1 output_$now.mkv 
sleep 0.5

done
