from skimage import morphology 
from skimage.measure import compare_ssim as ssim
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
from skimage.filters import gabor
import cv2
import os
import sys
threshold=0.79
ref_path="/home/shoban/Project/Ref/"
data_path="/home/shoban/Project/Data"
characters = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','remove','done','blank']
# Frame generation
#ffmpeg -i output_.mkv -r 6 thumb%04d.png -hide_banner

# Template Matching

# Loading Test Frames into a Tensor
def ld_ref_frames():
	ref=np.zeros((360,405,39))
	print ref.shape
	i=0
	for filename in sorted(os.listdir(ref_path)):
    		if filename.endswith(".png"): 
    			ref_img_path=os.path.join(ref_path, filename)
        		#print ref_img_path
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
			mask=cv2.imread("/home/shoban/Project/Threshold/template.png",flags=0)
			print mask.shape
			crop_img_mask=mask[360:720, 440:845]
			marker=data_img
                        crop_img_marker=marker[360:720, 440:845]
			cmp_img=crop_img_mask-crop_img_marker
			cmp_img=cv2.GaussianBlur(cmp_img,(5,5),1)
			#print cmp_img.dtype
			#test=ref[:,:,0]
			#print test.shape
			for i in range(0,39):
				#temp=ref[:,:,i]
				#print temp.dtype
				#cmp_out=ssim(ref[:,:,i],cmp_img)
				#print i
				if (done_chk==1):
					cmp_out_chk=ssim(ref[:,:,37],cmp_img)
					if (cmp_out_chk<0.28):
						done=1
						break
				else:
					cmp_out=ssim(ref[:,:,i],cmp_img)
					#print i
					#print cmp_out
					
					if (cmp_out>0.7955):
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
						elif (blank_yes==1)and(i==36) and(cmp_out>0.81):
							# Remove the last character in passwd
							passwd=passwd[:-1]
							print characters[i]
							blank_yes=0
							break
						elif (i==38 and cmp_out>0.80):
							blank_yes=1
							print characters[i]
							break
					if (i==37)and(blank_yes==1)and(cmp_out>0.77):
						done_chk=1
						print characters[i]
						break
					
				cmp_out=0
				
			if (done==1):
				return passwd
	return passwd

ref=ld_ref_frames()
passwd=cmp_frames(ref)
print passwd
"""
src_path="/home/shoban/junk/"

def filtering(img_path):

	img = cv2.imread(img_path)
	print img.shape
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((1,1), np.uint8)
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)

	#cv2.imwrite(src_path + "removed_noise.png", img)
	img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	cv2.imwrite(src_path + "thresh_test.png", img)



#result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))


#filtering(src_path + "thumb0001.png")
filtering(src_path + "thumb0080.png")

mask=cv2.imread("/home/shoban/Project/Threshold/thresh.png",flags=0)
print mask.shape
crop_img_mask=mask[400:720, 440:845]
#io.imshow(crop_img)
#plt.show()
#mask = np.asarray( mask, dtype="int32" )
marker=cv2.imread("/home/shoban/junk/thresh_test.png",flags=0)
crop_img_marker=marker[400:720, 440:845]
io.imshow(crop_img_marker)
plt.show()
#marker = np.asarray( marker, dtype="int32" )
#mask=morphology.skeletonize_3d(mask)
#marker=morphology.skeletonize_3d(marker)
rec=crop_img_mask-crop_img_marker
#rec=crop_img_marker-crop_img_mask
med=cv2.GaussianBlur(rec,(5,5),10)
#cv2.imwrite(src_path + "ref_test.png",med)
#'''
#a=cv2.imread("/home/shoban/Project/Ref/ref_u.png",flags=0)
#print a.shape
#b=cv2.imread("/home/shoban/junk/ref_test.png",flags=0)
#print b.shape
#print (ssim(a,b))
#print(ssim(a,a))
#filt_real, filt_img=gabor(rec, frequency=0.8)
# ssim > 88.2
io.imshow(med)
plt.show()
"""
