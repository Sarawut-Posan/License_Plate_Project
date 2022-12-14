import cv2
import numpy as np
import imutils 
from scipy.spatial import distance
import os
import datetime
from datetime import date
from datetime import datetime
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

def last_part(last,database1):
    
    last11 = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    wwlast, hwlast = last11.shape[::-1]
    last = last[round(hwlast/1.6):hwlast,1:wwlast]
    last_lpgg = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    ret, thresh_block_lpgg = cv2.threshold(last_lpgg, 100, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((2, 2), np.uint8)
    # Using cv2.erode() method 
    last_erode = cv2.erode(thresh_block_lpgg, kernel) 
    # Taking a matrix of size 5 as the kernel
    kernel = np.ones((3,3), np.uint8)
    last_erode = cv2.dilate(last_erode, kernel, iterations=1)

    contours = cv2.findContours(thresh_block_lpgg.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    #contours = sorted(contours,key=cv2.contourArea, reverse = True)[:5]
    screenCnt = None
    (cnts, boundingBoxes) = sort_contours(contours, method="left-to-right")
    count=42
    result=[]
    for c1 in cnts:
        count=count+1
        #print(count)
        # approximate the contour
        x1,y1,w1,h1 = cv2.boundingRect(c1)
        num1 = last_erode[y1:y1+h1, x1:x1+w1]
        filename = 'database1/' + str(count) + '.jpg'
        #cv2.imwrite(filename, num1)
        cv2.imshow("num1", num1)
        cv2.waitKey(0)
        leftmost = tuple(c1[c1[:,:,0].argmin()][0])
        rightmost = tuple(c1[c1[:,:,0].argmax()][0])
        topmost = tuple(c1[c1[:,:,1].argmin()][0])
        bottommost = tuple(c1[c1[:,:,1].argmax()][0])

        data_leftmost = [leftmost[0], leftmost[1]]
        data_rightmost = [rightmost[0], rightmost[1]]
        data_topmost = [topmost[0], topmost[1]]
        data_bottommost = [bottommost[0], bottommost[1]]

        datatest = [leftmost[0], leftmost[1],rightmost[0], rightmost[1],topmost[0], topmost[1],bottommost[0], bottommost[1]]
        print('datatest', datatest)

        dists=[]
        count1=0
        for ii in range(51):
            count1=count1+1
            dist = distance.euclidean(datatest,database1[ii])
            dists.append(dist)

        print('dists',dists)
        print('-----------------------')
        smallest = np.argmin(dists)
        print('smallest',smallest)
        print('-----------------------')

        #if smallest==0 or smallest==2 or smallest==3 or smallest==8 or smallest==10 or smallest==13 or smallest==14 or smallest==18 or smallest==21 or smallest==24 or smallest==27 or smallest==29 or smallest==31 or smallest==33 or smallest==34 or smallest==36 or smallest==37 or smallest==38 or smallest==41 or smallest==43 or smallest==45 or smallest==48 or smallest==50:
        target = ['4','','3','0','', #1-5
        '','','','4','', #ุ6-10
        '8','','','5','7', #11-15
        '','','','4','', #16-20
        '','8','','','8', #21-25
        '','','3','','2', #26-30
        '','2','','3','2', #31-35
        '','5','7','8','', #36-40
        '','7','','5','', #41-45
        '0','','','0','','3'] #46-51
        res = target[smallest]
        print('res',res)
        print('-----------------------')
        result.append(res)

    print('result',result)
    print('-----------------------')

    lens = len(result)
    ress=""
    for ik in range(lens):
        ress = ress + result[ik]
    print('ress',ress)

    return ress

def mid_part(mid):
    last11 = cv2.cvtColor(mid, cv2.COLOR_BGR2GRAY)
    wwlast, hwlast = last11.shape[::-1]
    last = mid[round(hwlast/2.6):round(hwlast/1.6),1:wwlast]
    last_lpgg = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    ret, thresh_block_lpgg = cv2.threshold(last_lpgg, 100, 255, cv2.THRESH_BINARY_INV)

    # Taking a matrix of size 5 as the kernel
    kernel = np.ones((3,3), np.uint8)
    last_erode = cv2.dilate(thresh_block_lpgg, kernel, iterations=2)
    contours = cv2.findContours(last_erode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours,key=cv2.contourArea, reverse = True)[:1]
    for c1 in contours:
        # approximate the contour
        x1,y1,w1,h1 = cv2.boundingRect(c1)
    print(w1)

    if w1>=48 and w1<=89:
        res = 'Ubonratchathani'
        print(res)
    if w1>=35 and w1 <=47:
        res = 'Sisaket'
    print(res)

    return res

def top_part(top):
    
    now = datetime.now() # current date and time

    year = now.strftime("%Y")
    print("year:", year)

    month = now.strftime("%m")
    print("month:", month)

    day = now.strftime("%d")
    print("day:", day)

    time = now.strftime("%H:%M:%S")
    print("time:", time)

    HH = now.strftime("%H")
    MM = now.strftime("%M")
    SS = now.strftime("%S")

    datess = str(day)+'_'+str(month)+'_'+str(year)+'_'
    timess = str(HH)+'_'+str(MM)+'_'+str(SS)	

    last11 = cv2.cvtColor(top, cv2.COLOR_BGR2GRAY)
    wwlast, hwlast = last11.shape[::-1]
    last = top[1:round(hwlast/2.6),1:wwlast]
    list = os.listdir("C:/Users/SP3th/OneDrive/Desktop/License Plate Projecy/lpr/top_part_image") # dir is your directory path
    number_files = len(list)
    filename = 'top_part_image/' + str(datess) + str(timess) + '.jpg'
    cv2.imwrite(filename, last)
    path_f = filename
    return path_f