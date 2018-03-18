#!/usr/bin/env python

############################################################################################
################# SCRIPT TO FIND THE UNLOCK PASSWORD OF A SMART PHONE ######################
############################################################################################
 

from skimage import morphology 
from skimage.measure import compare_ssim as ssim
from skimage import io
import numpy as np
import subprocess
from matplotlib import pyplot as plt
from skimage.filters import gabor
import cv2
import os
import sys


project_path="/home/shoban/Project/"
video_path="/home/shoban/Project/Videos/"
ref_path="/home/shoban/Project/Ref1/"
data_path="/home/shoban/Project/Data/"
template_main=cv2.imread("/home/shoban/Project/Threshold/template.png",flags=0)
template_home=cv2.imread("/home/shoban/Project/Threshold/template_home.png",flags=0)

characters = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','remove','done','blank']


# Template Matching
def frame_select():
	for filename in sorted(os.listdir(data_path)):
		if filename.endswith(".png"):
			img_path=os.path.join(data_path, filename)
			img=cv2.imread(img_path)
                	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                	kernel = np.ones((1,1), np.uint8)
                	img = cv2.dilate(img, kernel, iterations=1)
                	img = cv2.erode(img, kernel, iterations=1)
                        #cv2.imwrite(data_path + "removed_noise.png", img)
                	img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
			crop_temp_main=template_main[360:720, 440:845]
			crop_temp_home=template_home[360:720, 440:845]
			chk = cv2.matchTemplate(img,crop_temp_main,cv2.TM_CCOEFF_NORMED)
                	chk1 = cv2.matchTemplate(img,crop_temp_home,cv2.TM_CCOEFF_NORMED)
	        	compare= np.where( chk >= 0.7)
                	compare=np.asarray(compare)
                	compare1= np.where( chk1 >= 0.7)
                	compare1=np.asarray(compare1)
			if(compare.size>0 or compare1.size>0):
				continue
			else:
				os.remove(img_path)

# Loading Test Frames into a Tensor
def ld_ref_frames():
	ref=np.zeros((140,85,36))
	print ref.shape
	i=0
	for filename in sorted(os.listdir(ref_path)):
    		if filename.endswith(".png"):
			if(i>35):
				break 
    			ref_img_path=os.path.join(ref_path, filename)
        		#print ref_img_path
			#print i
        		ref[:,:,i]=cv2.imread(ref_img_path,flags=0)
        		i+=1
	ref = np.asarray(ref, dtype="uint8" )
	return ref

# Comparing data images with reference images
def cmp_frames(ref):
	blank_yes=1
	done=0
	done_chk=0
	passwd=""
	done_t=cv2.imread(ref_path+"zzz.png",flags=0)
	blank=cv2.imread(ref_path+"zzzz.png",flags=0)
	remove=cv2.imread(ref_path+"zz.png",flags=0)
	threshold=0.83
        for filename in sorted(os.listdir(data_path)):
                if filename.endswith(".png"): 
                        data_img_path=os.path.join(data_path, filename)
			print data_img_path
                        #print ref_img_path
                        data_img=cv2.imread(data_img_path)
			print data_img.shape
                        data_img = cv2.cvtColor(data_img, cv2.COLOR_BGR2GRAY)
        		kernel = np.ones((3,3), np.uint8)
        		data_img = cv2.dilate(data_img, kernel, iterations=1)
        		data_img = cv2.erode(data_img, kernel, iterations=1)
			#cv2.imwrite(data_path + "removed_noise.png", img)
        		data_img = cv2.adaptiveThreshold(data_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        		#cv2.imwrite(data_path + "thresh_test.png", data_img)
			mask=template_main
			print mask.shape
			crop_img_mask=mask[360:720, 440:845]
			marker=data_img
                        crop_img_marker=marker[360:720, 440:845]
			cmp_img=crop_img_mask-crop_img_marker
			cmp_img=cv2.GaussianBlur(cmp_img,(5,5),1)

			for i in range(0,39):
				#cmp_out=ssim(ref[:,:,i],cmp_img)
				#print i
				if (done_chk==1):
					#print "In"
					cmp_out_chk=ssim(blank,cmp_img)
					print cmp_out_chk
					if (cmp_out_chk<0.40):
						done=1
						break
				else:
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
					cmp_out= np.where( chk >= threshold)
					cmp_out1=np.asarray(cmp_out)
					#print cmp_out1.size
					if (cmp_out1.size>0):
						print "yes"
						if (blank_yes==1) and (i<36):
                                        		if(done_chk==1):
                                                		print "Incorrect Password"
                                                		passwd=""
                                                		done_chk=0

							print i
							print characters[i]
							passwd=passwd+str(characters[i])
							blank_yes=0
							break
						elif (blank_yes==1)and(i==36):
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

passwd_file=open(project_path + "password.txt","a+")
for filename in sorted(os.listdir(video_path)):
	if filename.endswith(".mkv"):
		command="sudo bash frame_gen.sh " + video_path + filename
		# Frame generation - Calls the script to generate the frames 
		subprocess.call(command, shell=True)
		# Selects useful frames needed to decipher the password
		frame_select()
		# Loads the reference templates into a reference variable
		ref=ld_ref_frames()
		# Processes the data frames, does template matching with reference templates and identifies the right character match
		passwd=cmp_frames(ref)
		print passwd
		passwd= (filename,)+passwd
		# Writing the password to a file
		passwd_file.write(str(passwd) + '\n')
passwd_file.close()


"""
frame_select()
ref=ld_ref_frames()
passwd=cmp_frames(ref)
print passwd

"""
