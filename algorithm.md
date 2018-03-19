---
layout: default
title: Algorithm
description: Algorithm
---



# 1. auto_record.sh

This script is used to continuously check if a phone is connected to the VGA2USB video grabber and record the video.
In this script `ffmpeg` package is used to record the video. This script identifies if a phone is connected to the video grabber from the standard output of the `ffmpeg`.

**Pseudo code of the script is as follows:**
```
# The error.txt is the file that stores the standard output of `ffmpeg`. Deleting any revious copies of error.txt
if any error.txt exist: 
	delete error.txt 

# Function to check if a phone is connected to VGA2USB
isconnected()
{

if error.txt not present in the folder:
	return 0 # To indicate the script has just started, it has to run ffmepg to generate the error.txt
else	
	if error.txt contains "Last message repeated|No medium found|Dequeued v4l2 buffer contains corrupted data": - These commands mean no phone connected to VGA2USB
		print device disconnected
    	pid=`pidof ffmpeg` - getting the process id of last ffmpeg command
        sudo kill -9 $pid - Killing that last ffmpeg process, this will save the last video
		remove the error.txt - To start fresh when a new connection comes
		return 1
	else
		print Device connected
		return 1
}

# isconnected =1 means phone is connected to the VGA2USB device else no connection.

while[1]{
	now= current date and time
	# If no device is connected, try starting a new recording, as ffmpeg throws an error if no connection, else records
	if ! isconnected:
		ffmpeg -framerate 10 -analyzeduration 2 -f v4l2 -i /dev/video1 /home/shoban/Project/Videos/output_$now.mkv >& error.txt & - records video at 10fps and outputs to error.txt
	else
		Device Connected
		continue
}
```

# 2. frame_gen.sh

This script is used to convert the recorded video into frames at a suitable frame rate

**Pseudocode is as follows:**
```
if there are data frames:
	delete previous data frames # This is done so that new frames mix with the old data frames
	
# Generates frame at 6 frame/sec with the name starting with vid and 5 digit counter value
ffmpeg -i $1 -r 6 /home/shoban/Project/Data/vid%05d.png -hide_banner

# Moves the processed video into archives
sudo mv $1 /home/shoban/Project/Videos/Archives/
```

# 3. password_extract.py

This script is used to extract the unlock password from the generated data frames.

**Pseudocode is as follows:**
```
data_path= path where the frames containing password information are stored
video_path= path where the videos from the phone are stored

template_main= Load the sample template for the main unlock screen
template_home = Load the sample template for the home screen 

# To select the frames needed to detect the password and remove the rest
frame_select(){
	for all the files in data path:
		if the filename ends with .png:
			img= read the image with .png extn
			img=rgb2gray(img) # Converting the img to grayscale
			# Performing morphological techniques to obtain the skeleton of the image 
			img=dilate(img)
			img=erode(img)
			# Apply adaptive thresholding to filter the image from noise
			img = adaptiveThreshold(img)
			crop_img_main=crop(template_main, [360:720, 440:845]) # Retain only the lower half of the frame
			crop_img_home=crop(template_home, [360:720, 440:845]) # Retain only the lower half of the frame
			chk1=Template matching (crop_img_home, img)
			chk2=Template matching (crop_img_main, img)
			if chk1 and chk2 >0.7:
				continue
			else
				remove that img - frame not needed
}

# Loading reference templates
ld_ref_frames(){

Load all the reference templates of the characters on the keyboard into ref[:,:,39]

}	

# Comparing the data images with reference images

cmp_frames(ref){

	for all the files in data path:
		if the filename ends with .png:
			img= read the image with .png extn
			img=rgb2gray(img) # Converting the img to grayscale
			# Performing morphological techniques to obtain the skeleton of the image 
			img=dilate(img)
			img=erode(img)
			# Apply adaptive thresholding to filter the image from noise
			img = adaptiveThreshold(img)
			mask=template_main
			crop_img_mask=crop(mask, [360:720, 440:845]) # Retain only the lower half of the frame - Keyboard
			crop_img_marker=crop(img, [360:720, 440:845]) # Retain only the lower half of the frame - Keyboard
			cmp_img=crop_img_mask-crop_img_marker # Subtracting the template from the data image to obtain the character pressed
			cmp_img=cv2.GaussianBlur(cmp_img,(5,5),1) # Filtering the key pressed to remove noise
			
			# Comparing each data frame with each of 39 reference templates using template matching
			for i in range(0,39):
				# T0 check if the user has pressed the "done" key 
				if (done_chk==1):
					Compare the incoming frame with the black keyboard screen, if false, the password is correct
					break
				else:
				    # Setting threshold depending on the characters, remove button, done button, or blank keyboard screen and computing template matching 
					if(i<36):
						threshold=0.896
						chk = cv2.matchTemplate(cmp_img,ref[:,:,i],cv2.TM_CCOEFF_NORMED)
					elif(i==36):
						threshold=0.91
						chk = cv2.matchTemplate(cmp_img,remove,cv2.TM_CCOEFF_NORMED)
					elif(i==37):
						threshold=0.9
						chk = cv2.matchTemplate(cmp_img,done_t,cv2.TM_CCOEFF_NORMED)
					elif(i==38):
						threshold=0.7
						chk = cv2.matchTemplate(cmp_img,blank,cv2.TM_CCOEFF_NORMED)
					# Checking the Template matching output with the threshold
					if (chk > threshold):
						print "yes"
						# TO check if the previous frame was a blank frame and if the key pressed is a character
						if (blank_yes==1) and (i<36):
							# If previously done button is pressed and if control comes here, it means incorrect password
                            if(done_chk==1):
                                print "Incorrect Password"
                                passwd=""
                                done_chk=0
								
							passwd=passwd+str(characters[i])
							blank_yes=0
							break
						elif (blank_yes==1)and(i==36): i= 36 #refers to remove character
							# Remove the last character in passwd
							passwd=passwd[:-1]
							print characters[i]
							blank_yes=0
							break
						elif (i==38):
							blank_yes=1
							print characters[i]
							break
						elif (i==37)and(blank_yes==1):
							done_chk=1
							print characters[i]
							break
					
				cmp_out=[]
			print done	
			if (done==1):
				return ("Correct password", passwd)
	return ("Incorrect Password", passwd)
}

passwd_file=open password.txt file
for filename in video_path
	if filename.endswith(".mkv"):
		call frame_gen.sh to generate frames
		# Selects useful frames needed to decipher the password
		frame_select()
		# Loads the reference templates into a reference variable
		ref=ld_ref_frames()
		# Processes the data frames, does template matching with reference templates and identifies the right character match
		passwd=cmp_frames(ref)
		passwd= (filename,)+passwd
		# Writing the password to a file
		passwd_file.write(str(passwd) + '\n')
passwd_file.close()
			
```
	

