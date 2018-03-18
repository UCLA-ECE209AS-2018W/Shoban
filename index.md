---
layout: default
title: About the Project
description: Project objective and Goals
---
![About the Project](about.jpg)

# Deep Hyperspectral Imager

## Objective
To create  an imaging device that augments RGB cameras with additional non-imaging modalities such as RF, acoustic, depth and thermal.
Each of these modalities provide different information about the scene and the project aims to create a platform to fuse these multimodal images and train the platform for object detection.

## Specific goals:
1. Map a source of sound in 3D space by making use of beamforming micro phone arrays
2. Obtain RF, thermal and depth images of the scene
3. Calibrate the imaging sensors in a way that they cover a specific field of view in the scene.
4. Integrate the imaging sensors into a single platform
5. Train the hyperspectral imaging platform for object detection

## Contents
  1. [Components](components.md)
  2. [Getting Started with NVIDIA Jetson Tx2](getting_started.md)
  3. Implementation: Individual sensor calibration and implementation
     * [Microphone Array - Matrix](Matrix.md)
     * [RF mmWave sensor (TI IWR1642)](RF_mmwave.md)
     * [Time of Flight Camera (Intel Realsense SR300)](Realsense_sr300.md)
     * [Thermal Camera (FLIR Dev Kit)](flir.md)
  4. [Sensor Output](sensor_output.md)
  5. [Multi Modal Images](multimodal.md)
  6. [Timeline](timeline.md)
  7. [References](references.md)

## Project Members
1. **Aman Srivastava**
2. **Shoban Narayan Ramesh**
3. **Shreya Ramaprasad**

## Project Mentor
**Prof. Mani Srivastava**

## Contributions and Efforts
* Sound Localisation: Shreya Ramaprasad
* Modality overlay algorithm, frame size and Calibration : Aman Srivastava, Shoban Narayan Ramesh and Shreya Ramaprasad
* Intel Realsense Camera and Jetson TX2 setup : Shoban Narayan Ramesh
* FLiR Thermal camera and Kinect configuration on Pi: Aman Srivastava

* A special thanks to **Amr(student of Prof Mani Srivastava)** for guiding us throughout this project.
