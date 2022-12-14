#!/usr/bin/env python
import cv2
import mysql.connector
import numpy as np
import time

import cv2
import numpy as np
import imutils 
from scipy.spatial import distance
from part import last_part
from part import mid_part
from part import top_part
import mysql.connector
import subprocess, sys
import os
import datetime

#Load YOLO
net = cv2.dnn.readNet("config_helmet/yolo_last.weights","config_helmet/yolo.2.0-obj.cfg") # Original yolov3
classes = []
with open("config_helmet/obj.names","r") as f:
    classes = [line.strip() for line in f.readlines()]

print(classes)

layer_names = net.getLayerNames()
outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


colors= np.random.uniform(0,255,size=(len(classes),3))

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

database1 = [[5, 14, 15, 17, 9, 5, 12, 18],
[7, 15, 12, 9, 10, 7, 11, 16],
[18, 5, 28, 17, 20, 4, 20, 18],
[32, 4, 42, 16, 33, 3, 33, 17],
[34, 13, 40, 7, 36, 4, 39, 15],
[1, 0, 23, 21, 1, 0, 1, 21],
[10, 13, 12, 17, 10, 13, 11, 17],
[10, 16, 12, 16, 11, 15, 11, 17],
[22, 11, 32, 13, 28, 3, 29, 15],
[24, 10, 29, 9, 27, 7, 27, 12],
[36, 5, 46, 15, 37, 4, 45, 16],
[38, 11, 44, 11, 39, 10, 43, 15],
[38, 7, 43, 6, 40, 4, 42, 9],
[50, 4, 60, 15, 50, 4, 56, 16],
[64, 4, 74, 7, 64, 4, 67, 16],
[1, 0, 6, 24, 1, 0, 1, 24],
[10, 0, 11, 12, 10, 0, 11, 18],
[13, 24, 82, 24, 56, 20, 13, 24],
[22, 14, 33, 16, 29, 5, 29, 19],
[24, 14, 30, 15, 27, 11, 29, 16],
[30, 23, 45, 22, 36, 21, 38, 24],
[37, 6, 47, 16, 39, 5, 38, 18],
[39, 13, 45, 14, 40, 12, 42, 18],
[39, 7, 44, 7, 40, 6, 43, 10],
[51, 14, 62, 15, 54, 4, 53, 18],
[53, 14, 60, 14, 56, 11, 58, 17],
[53, 8, 59, 7, 55, 5, 56, 10],
[67, 5, 77, 14, 70, 3, 68, 17],
[1, 0, 31, 24, 1, 0, 1, 24],
[22, 5, 32, 17, 24, 3, 28, 17],
[36, 22, 43, 23, 36, 22, 41, 23],
[36, 5, 46, 18, 38, 4, 38, 18],
[45, 23, 45, 23, 45, 23, 45, 23],
[49, 14, 59, 18, 52, 5, 52, 19],
[63, 19, 74, 21, 66, 6, 73, 21],
[1, 0, 93, 26, 1, 0, 1, 26],
[25, 5, 38, 15, 35, 4, 28, 19],
[41, 5, 53, 6, 42, 4, 45, 19],
[59, 5, 71, 14, 63, 3, 61, 18],
[61, 14, 68, 13, 63, 11, 66, 16],
[61, 7, 67, 6, 64, 4, 65, 9],
[75, 3, 87, 5, 81, 2, 78, 17],
[1, 0, 12, 39, 1, 0, 1, 39],
[32, 11, 48, 27, 37, 10, 36, 30],
[35, 2, 36, 3, 35, 2, 35, 3],
[54, 14, 69, 21, 59, 9, 60, 29],
[57, 21, 65, 15, 60, 12, 62, 26],
[58, 39, 117, 39, 113, 35, 70, 39],
[75, 12, 90, 19, 80, 7, 80, 27],
[78, 20, 87, 16, 81, 10, 83, 24],
[96, 9, 111, 21, 99, 6, 102, 26]]

#loading image
cap = cv2.VideoCapture(0) #0 for 1st webcam
font = cv2.FONT_HERSHEY_PLAIN
starting_time= time.time()
frame_id = 0

while True:
    _,frame= cap.read() #
    frame_for_lpr = frame 
    frame_id+=1
    
    height,width,channels = frame.shape
    #detecting objects
    blob = cv2.dnn.blobFromImage(frame,0.00392,(320,320),(0,0,0),True,crop=False) #reduce 416 to 320    

        
    net.setInput(blob)
    outs = net.forward(outputlayers)
    #print(outs[1])


    #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
    class_ids=[]
    confidences=[]
    boxes=[]
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                print("det >",detection )

                #print(confidence)
                #onject detected
                center_x= int(detection[0]*width)
                center_y= int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                #rectangle co-ordinaters
                x=int(center_x - w/2)
                y=int(center_y - h/2)
                #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                boxes.append([x,y,w,h]) #put all rectangle areas
                confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                class_ids.append(class_id) #name of the object tha was detected

                if class_id == 0:
                   #print("Grade B")
                   cv2.putText(frame,"Grade B",(5,29),font,2,(255,0,255),4)

                elif class_id == 1:
                   #print("Grade C")
                   cv2.putText(frame,"Grade C",(5,29),font,2,(255,0,255),4)

                else:
                   #print("Grade A")
                   cv2.putText(frame,"Grade A",(5,29),font,2,(255,0,255),4)

               
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

   
    for i in range(len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence= confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y+30),font,1,(0,0,255),2)
            

    elapsed_time = time.time() - starting_time
    fps=frame_id/elapsed_time
    #cv2.putText(frame,"FPS:"+str(round(fps,2)),(5,15),font,1,(0,255,0),1)

    # Find car on image for devide part 
    # Read the main image
    img_rgb = frame_for_lpr #1, 2,32, 43, 50, 68, 69, 78, 79, 80 , 81, 88, 89, 90, 93
    img_rgb = imutils.resize(img_rgb,height=500) # 50, 68, 79 , 80, 88, 89
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

    xdate = datetime.datetime.now()
    print(xdate)
    last = img_rgb[y:y+h, x:x+w]
    lastresult = last_part(last,database1)
    midresult = mid_part(last)
    path_f = top_part(last)

    mydb = mysql.connector.connect(
        host="jassada.cdqqutbe7d4o.us-east-2.rds.amazonaws.com",
        user="root", 
        passwd="taaisasvmw45120",
        database="LPR",
        auth_plugin='mysql_native_password'
        )  
    mycursor = mydb.cursor()
    sql = "INSERT INTO lpr_name(dates,number,city,top_part_file) VALUES (%s,%s,%s,%s)"
    val = (xdate, lastresult, midresult,path_f)
    mycursor.execute(sql, val)   
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    
    cv2.imshow("Image",frame)
    key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame
    
    if key == 27: #esc key stops the process
    break
    
cap.release()    
cv2.destroyAllWindows()
