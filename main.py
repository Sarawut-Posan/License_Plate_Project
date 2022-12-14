import os
import cv2
from matplotlib import pyplot as plt
import numpy as np
import pytesseract
import imutils 
from scipy.spatial import distance
from Part import top_part
from Part import mid_part

gray = cv2.imread("C:/Users/SP3th/OneDrive/Desktop/License Plate Projecy/lpr/1.JPG", 0)
gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(gray, (5,5), 0)
gray = cv2.medianBlur(gray, 3)
# perform otsu thresh (using binary inverse since opencv contours work better with white text)
ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
cv2.imshow("Otsu", thresh)
cv2.waitKey(0)
rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

# apply dilation 
dilation = cv2.dilate(thresh, rect_kern, iterations = 1)
#cv2.imshow("dilation", dilation)
#cv2.waitKey(0)
# find contours
try:
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
except:
    ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])


img = cv2.imread("/Users/pond/Desktop/FinalProject/Data/RealData/img1.JPG")
  
# cv2.imread() -> takes an image as an input
h, w, channels = img.shape
  
# saving all the images
# cv2.imwrite() function will save the image 
# into your pc
cv2.imwrite('top.jpg', top)
cv2.imwrite('bottom.jpg', bottom)
cv2.waitKey(0)

# create copy of image
im2 = gray.copy()

plate_num = ""
plate_province = ""
# loop through contours and find letters in license plate
for cnt in sorted_contours:
    x,y,w,h = cv2.boundingRect(cnt)
    height, width = im2.shape
    
    # if height of box is not a quarter of total height then skip
    if height / float(h) > 6: continue
    ratio = h / float(w)
    # if height to width ratio is less than 1.25 skip
    if ratio < 1.25: continue
    area = h * w
    # if width is not more than 25 pixels skip
    if width / float(w) > 25: continue
    # if area is less than 100 pixels skip
    if area < 100: continue
    # draw the rectangle
    rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),2)
    roi = thresh[y-5:y+h+5, x-5:x+w+5]
    roi = cv2.bitwise_not(roi)
    roi = cv2.medianBlur(roi, 5)
    #cv2.imshow("ROI", roi)
    #cv2.waitKey(0)
    config="-l tha --psm 7"
    text = pytesseract.image_to_string(roi, config=config)
    #print(text)
    plate_num += text
print("number : ", plate_num.replace("\n", " "))

for cnt2 in sorted_contours:
    x,y,w,h = cv2.boundingRect(cnt2)
    height, width = im2.shape
    
    # if height of box is not a quarter of total height then skip
    if height / float(h) < 6: continue
    ratio = h / float(w)
    # if height to width ratio is less than 1.25 skip
    if ratio < 1: continue
    area = h * w
    # if width is not more than 25 pixels skip
    if width / float(w) < 12.5: continue
    # if area is less than 100 pixels skip
    if area < 100: continue
    # draw the rectangle
    rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),1)
    roi = thresh[y-10:y+h+10, x-1:x+w+1]
    roi = cv2.bitwise_not(roi)
    roi = cv2.medianBlur(roi, 5)
    #cv2.imshow("ROI", roi)
    #cv2.waitKey(0)
    config="-l tha --psm 6"
    text = pytesseract.image_to_string(roi, config=config)
    #print(text)
    plate_province += text
print("province : ", plate_province.replace("\n", " "))

cv2.imshow("Character's Segmented", im2)
cv2.waitKey(0)


    