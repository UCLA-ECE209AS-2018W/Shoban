---
layout: default
title: Challenges
description: Challenges
---



# Challenges


-	**Epiphan VGA2USB driver** – This company has stopped making drivers for recent kernel versions of Raspberry Pi and Ubuntu, since they support only an old kernel version, I was forced to load an old kernel module on top of my recent one to have this driver working. \[[9](/references.md)\] 

-	**Choosing a suitable frame rate** – Frame rate was difficult to choose as more was the frame rate, there were more frames having the same key presses, this would lead to multiple key detections. Having a lower frame rate sometimes drops the key presses if the keys are pressed quickly. In order to strike a balance I chose a frame rate of 10 for recording, 6 for converting the video into frames and used to detect blank frames in between key presses to eliminate duplicate detections.

-	**Frame Comparisons** - Choosing the right technique for frame comparison was another challenge, where implementing Optical Character Recognition would have been a generalized approach, giving the scalability to extend to any keyboard but it had very poor accuracy and I had to choose between Structural similarity and Template matching.
