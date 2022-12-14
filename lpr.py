import cv2
import numpy as np
import imutils 
from scipy.spatial import distance
from part import last_part
from part import mid_part
from part import top_part
import mysql.connector
import subprocess, sys

def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

database1 = [[28, 6, 35, 21, 32, 2, 34, 21],[46, 4, 60, 20, 49, 2, 48, 20], [66, 6, 80, 19, 69, 2, 68, 20],
[23,8,32,23,27,4,28,23],[40,7,54,21,42,4,42,24],[59,15,74,20,63,3,61,23],[78,8,94,22,82,3,78,23]]

# Find car on image for devide part 
# Read the main image
img_rgb = cv2.imread('bicycle/bicycle/93.jpg') #1,2,32, 43, 50, 68, 69, 78, 79, 80 , 81, 88, 89, 90, 93
img_rgb = imutils.resize(img_rgb,height=500)
img_rgb2=img_rgb
img_rgbgg = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
ww, hw = img_rgbgg.shape[::-1]
img_rgb=img_rgb[50:hw,1:ww]
BLUnit = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
BLTen = cv2.blur(BLUnit, (3, 3))
BLUnitG = BLUnit
sobelxBLUnit = cv2.Sobel(BLTen,cv2.CV_8U,1,0,ksize=3)
ret2,threshold_imgBLUnit = cv2.threshold(sobelxBLUnit,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(17, 1))
morph_img_thresholdBLUnit = threshold_imgBLUnit.copy()
cv2.morphologyEx(src=threshold_imgBLUnit, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_thresholdBLUnit)
# Creating kernel
kernel = np.ones((5, 5), np.uint8)
# Using cv2.erode() method 
morph_img_thresholdBLUnit = cv2.erode(morph_img_thresholdBLUnit, kernel) 

# Taking a matrix of size 5 as the kernel
kernel = np.ones((15,15), np.uint8)
morph_img_thresholdBLUnit1 = cv2.dilate(morph_img_thresholdBLUnit, kernel, iterations=1)

contoursBLUnit = cv2.findContours(morph_img_thresholdBLUnit1.copy(),cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
contoursBLUnit = imutils.grab_contours(contoursBLUnit)
contoursBLUnit = sorted(contoursBLUnit,key=cv2.contourArea, reverse = True)[:1]
screenCnt = None
for c in contoursBLUnit:
    # approximate the contour
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img_rgb,(x,y),(x+w,y+h),(0,255,0),2)

block_lp = img_rgb2[y:y+h, x:x+w]
top = block_lp[1:25,1:200]
mid = block_lp[26:50,1:200]
last = block_lp[51:100,1:200]

topresult = top_part(top)
print(topresult)
midresult = mid_part(mid)
print(midresult) 
lastresult = last_part(last)
print(lastresult)

cv2.imshow("img_rgb", img_rgb)
cv2.imshow("block_lp", block_lp)
#cv2.imshow("thresh_block_lpgg", thresh_block_lpgg)
cv2.imshow("top", top)
cv2.imshow("mid", mid)
#cv2.imshow("thresh_block_lpgg", thresh_block_lpgg)

cv2.waitKey(0)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root", 
    passwd="12345678",
    database="lpr",
    auth_plugin='mysql_native_password'
	) 
mycursor = mydb.cursor()
sql = "INSERT INTO lpr(name,provide,lp) VALUES (%s,%s,%s)"
val = (topresult,midresult,midresult)
mycursor.execute(sql, val)   
mydb.commit()
print(mycursor.rowcount, "record inserted.")

'''
# Open the file in append mode
file = open("recognized.txt", "a")
# Apply OCR on the cropped image
text = pytesseract.image_to_string(last)
# Appending the text into file
file.write(text)
file.write("\n") 
# Close the file
file.close

cv2.imshow("img_rgb", img_rgb)

cv2.imshow("sobelxBLUnit", sobelxBLUnit)
cv2.imshow("threshold_imgBLUnit", threshold_imgBLUnit)
cv2.imshow("morph_img_thresholdBLUnit", morph_img_thresholdBLUnit)

cv2.imshow("block_lp", block_lp)
cv2.imshow("thresh_block_lpgg", thresh_block_lpgg)
cv2.imshow("top", top)
cv2.imshow("mid", mid)
cv2.imshow("last", last)
cv2.imshow("last_erode", last_erode)
cv2.imshow("num1", num1)
cv2.waitKey(0)
'''