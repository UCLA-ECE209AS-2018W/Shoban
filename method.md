---
layout: default
title: Method
description: Methodology
---

# Methodology

The linux driver of Epiphan’s VGA2USB for Ubuntu (64bit 4.10.0-28 kernel version) was [installed from here](https://ssl.epiphan.com/downloads/linux/). 
A linux package called ffmpeg which supports Video4Linux is used to record the video grabbed by the VGA2USB device and it is installed using the command `sudo apt-get install ffmpeg`. \[[1](/references.md)\]
This project has three scripts:
  1.  Auto_record.sh
  2.  Frame_gen.sh
  3.  Password_extract.py
  
## Video Recording
Having installed ffmpeg package a bash script called **auto_record.sh** was written, which continuously detects if there is an incoming video signal and records it. Whenever the video signal is disconnected, implying the phone is removed from the charger, the recorded video is saved with a name having the recorded date and time. Further this script is added to the **rc.local** file of ubuntu so that, this script begins to run at the start of the system after the completion of its boot.

## Video Processing
The recorded video is then divided into frames and saved at a particular location using the same ffmpeg package used to record the video. This is governed by the script **frame_gen.sh**.
Once the frames are recorded, they have to be further processed to extract the unlock passwords of the phone. This activity is taken care of by the script **password_extract.py**. In this script the frames are first filtered to have only the frames that contain the unlock password related information using template matching of the keyboard. 
There are a couple of techniques to recognize the characters pressed, some of them are \[[5](/references.md)\] and \[[6](/references.md)\]:
  -	 **Structural Similarity** (ssim)
  -	 **Mean Squared Error** \[[7](/references.md)\]
  -	 **Template Matching**
  -	 **Optical Character recognition**
  
1. Optical character recognition can be implemented with the package named pytesseract and this technique is a generalised technique which can recognise the key presses of any keyboard. However when I tried implementing this method its accuracy was really poor and it threw garbage values. \[[8](/references.md)\]
2. For instance, I had an image with the character “s” being pressed and the output of pytesseract was something like this - **Add a picture**
3. I implemented the logic for password extraction with structural similarity \[[7](/references.md)\] as well and found it had an accuracy better than the optical character recognition, however this technique will work only with the trained keyboard reference images and cannot be extended to the same keyboard of another phone or other keyboards.
4. Mean squared error is a poor measure of comparing two images, it only gives the perceived errors and not a direct measure of their similarity.
5. The technique used in this project to recognize the characters pressed on the keyboard is **Template Matching**. I used this techniques since it had really good accuracy in prediction and it can be applied to any standard qwerty keyboard. \[[4](/references.md)\]
On applying template matching, further logic was applied to detect incorrect passwords, removal of characters while typing.
