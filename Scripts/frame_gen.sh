#!/usr/bin/env bash

# A script to generate frames from video


# To deleete any previous data frames
if ! [ -z "/home/shoban/Project/Data" ]
then
	sudo rm /home/shoban/Project/Data/*
fi 
# Generates frame at 6 frame/sec
ffmpeg -i $1 -r 6 /home/shoban/Project/Data/vid%05d.png -hide_banner
# Moves the video into archives
sudo mv $1 /home/shoban/Project/Videos/Archives/
