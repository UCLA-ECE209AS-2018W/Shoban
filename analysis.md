---
layout: default
title: Analysis
description: Analysing the results
---

# Analysis


-	It can be seen from the results that a new video is recorded the each time the device is connected to the charger and the video is named with the time and date of recording. However it doesn’t have a device ID to track if the same device is connected and hence multiple entries can exist in the password.txt for the same device. These entries have to be manually verified by watching the video to check if they belong to the same device. 
-	Frame rate selected for video recording is 10 fps. This is chosen from the specification of the VGA2USB grabber. This device supports a maximum frame rate of 28, which has the least resolution of 640x480. In order to strike a balance between better resolution and frame rate, frame rate was chosen to be as 10, which gives a resolution of 1024x768. The specifications of the epiphan’s VGA2USB video grabber [can be seen here](https://www.epiphan.com/products/vga2usb/tech-specs/). 
-	The results obtained depend on the **speed of typing** and the **pressure applied while pressing the keys**. It can be seen from the results (in password.txt) that when the speed of typing is too fast or if enough pressure is not applied while typing, the code is unable to detect the character and the character is missed in the final password written in password.txt. This is either because the frames obtained from the video drops the key press due to low frame rate used to convert the fast key presses or because the keys are pressed with lesser pressure and the pressed keys aren’t clearly visible in the frame for the template matching to identify.
