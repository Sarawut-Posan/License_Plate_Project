# GenData.py
# -*- coding: UTF-8 -*-

import sys
import numpy as np
import cv2
import os


# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30


###################################################################################################
def main():
    imgTrainingNumbers = cv2.imread("font photo remake_Li.jpg")  # read in training numbers image

    if imgTrainingNumbers is None:  # if image was not read successfully
        print("error: image not read from file \n\n")  # print error message to std out
        os.system("pause")  # pause so user can see error message
        return  # and exit function (which exits program)
    # end if

    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)  # get grayscale image
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)  # blur

    # filter image from grayscale to black and white
    imgThresh = cv2.adaptiveThreshold(imgBlurred,  # input image
                                      255,  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,
                                      # invert so foreground will be white, background will be black
                                      11,  # size of a pixel neighborhood used to calculate threshold value
                                      2)  # constant subtracted from the mean or weighted mean

    cv2.imshow("imgThresh", imgThresh)  # show threshold image for reference

    imgThreshCopy = imgThresh.copy()  # make a copy of the thresh image, this in necessary b/c findContours modifies the image

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,
                                                              # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                              cv2.RETR_EXTERNAL,  # retrieve the outermost contours only
                                                              cv2.CHAIN_APPROX_SIMPLE)  # compress horizontal, vertical, and diagonal segments and leave only their end points

    # declare empty numpy array, we will use this to write to file later
    # zero rows, enough cols to hold all image data
    npaFlattenedImages = np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    intClassifications = []  # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end

    # possible chars we are interested in are digits 0 through 9, put these in list intValidChars
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z'), ord('a'), ord('b'), ord('c'), ord('d'),
                     ord('e'), ord('f'), ord('g'), ord('h'), ord('i'), ord('j'), ord('k'), ord('l'), ord('m'), ord('n'), ord('o'),
                     ord('p'), ord('q'), ord('r'), ord('s'), ord('t'), ord('u'), ord('v'), ord('w'), ord('x'), ord('y'), ord('z'),
                     ord('+'), ord('!'), ord('*'), ord('/'), ord(','), ord('.'), ord(';'), ord('['), ord(']'), ord('{'), ord('}'),
                     ord('#')]

    for npaContour in npaContours:  # for each contour
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:  # if contour is big enough to consider
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)  # get and break out bounding rect

            # draw rectangle around each contour as we ask user for input
            cv2.rectangle(imgTrainingNumbers,  # draw rectangle on original training image
                          (intX, intY),  # upper left corner
                          (intX + intW, intY + intH),  # lower right corner
                          (0, 0, 255),  # red
                          2)  # thickness

            imgROI = imgThresh[intY:intY + intH, intX:intX + intW]  # crop char out of threshold image
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH,
                                                RESIZED_IMAGE_HEIGHT))  # resize image, this will be more consistent for recognition and storage

            cv2.imshow("imgROI", imgROI)  # show cropped out char for reference
            cv2.imshow("imgROIResized", imgROIResized)  # show resized image for reference
            cv2.imshow("training_numbers.png",
                       imgTrainingNumbers)  # show training numbers image, this will now have red rectangles drawn on it

            intChar = cv2.waitKey(0)  # get key press

            if intChar == 45:  # if esc key was pressed
                sys.exit()  # exit program
            elif intChar in intValidChars:  # else if the char is in the list of chars we are looking for . . .
                if intChar == ord('A'):
                    intChar = ord(u'ก')
                    print(unichr(intChar))
                if intChar == ord('B'):
                    intChar = ord(u'ข')
                    print(unichr(intChar))
                if intChar == ord('C'):
                    intChar = ord(u'ฃ')
                    print(unichr(intChar))
                if intChar == ord('D'):
                    intChar = ord(u'ค')
                    print(unichr(intChar))
                if intChar == ord('E'):
                    intChar = ord(u'ฅ')
                    print(unichr(intChar))
                if intChar == ord('F'):
                    intChar = ord(u'ฆ')
                    print(unichr(intChar))
                if intChar == ord('G'):
                    intChar = ord(u'ง')
                    print(unichr(intChar))
                if intChar == ord('H'):
                    intChar = ord(u'จ')
                    print(unichr(intChar))
                if intChar == ord('I'):
                    intChar = ord(u'ฉ')
                    print(unichr(intChar))
                if intChar == ord('J'):
                    intChar = ord(u'ช')
                    print(unichr(intChar))
                if intChar == ord('K'):
                    intChar = ord(u'ซ')
                    print(unichr(intChar))
                if intChar == ord('L'):
                    intChar = ord(u'ฌ')
                    print(unichr(intChar))
                if intChar == ord('M'):
                    intChar = ord(u'ญ')
                    print(unichr(intChar))
                if intChar == ord('N'):
                    intChar = ord(u'ฏ')
                    print(unichr(intChar))
                if intChar == ord('O'):
                    intChar = ord(u'ฎ')
                    print(unichr(intChar))
                if intChar == ord('P'):
                    intChar = ord(u'ฐ')
                    print(unichr(intChar))
                if intChar == ord('Q'):
                    intChar = ord(u'ฑ')
                    print(unichr(intChar))
                if intChar == ord('R'):
                    intChar = ord(u'ฒ')
                    print(unichr(intChar))
                if intChar == ord('S'):
                    intChar = ord(u'ณ')
                    print(unichr(intChar))
                if intChar == ord('T'):
                    intChar = ord(u'ด')
                    print(unichr(intChar))
                if intChar == ord('U'):
                    intChar = ord(u'ต')
                    print(unichr(intChar))
                if intChar == ord('V'):
                    intChar = ord(u'ถ')
                    print(unichr(intChar))
                if intChar == ord('W'):
                    intChar = ord(u'ท')
                    print(unichr(intChar))
                if intChar == ord('X'):
                    intChar = ord(u'ธ')
                    print(unichr(intChar))
                if intChar == ord('Y'):
                    intChar = ord(u'น')
                    print(unichr(intChar))
                if intChar == ord('Z'):
                    intChar = ord(u'บ')
                    print(unichr(intChar))
                if intChar == ord('a'):
                    intChar = ord(u'ป')
                    print(unichr(intChar))
                if intChar == ord('b'):
                    intChar = ord(u'ผ')
                    print(unichr(intChar))
                if intChar == ord('c'):
                    intChar = ord(u'ฝ')
                    print(unichr(intChar))
                if intChar == ord('d'):
                    intChar = ord(u'พ')
                    print(unichr(intChar))
                if intChar == ord('e'):
                    intChar = ord(u'ฟ')
                    print(unichr(intChar))
                if intChar == ord('f'):
                    intChar = ord(u'ภ')
                    print(unichr(intChar))
                if intChar == ord('g'):
                    intChar = ord(u'ม')
                    print(unichr(intChar))
                if intChar == ord('h'):
                    intChar = ord(u'ย')
                    print(unichr(intChar))
                if intChar == ord('i'):
                    intChar = ord(u'ร')
                    print(unichr(intChar))
                if intChar == ord('j'):
                    intChar = ord(u'ล')
                    print(unichr(intChar))
                if intChar == ord('k'):
                    intChar = ord(u'ว')
                    print(unichr(intChar))
                if intChar == ord('l'):
                    intChar = ord(u'ศ')
                    print(unichr(intChar))
                if intChar == ord('m'):
                    intChar = ord(u'ส')
                    print(unichr(intChar))
                if intChar == ord('r'):
                    intChar = ord(u'ษ')
                    print(unichr(intChar))
                if intChar == ord('n'):
                    intChar = ord(u'ห')
                    print(unichr(intChar))
                if intChar == ord('o'):
                    intChar = ord(u'ฬ')
                    print(unichr(intChar))
                if intChar == ord('p'):
                    intChar = ord(u'อ')
                    print(unichr(intChar))
                if intChar == ord('q'):
                    intChar = ord(u'ฮ')
                    print(unichr(intChar))
                if intChar == ord('s'):
                    intChar = ord(u'โ')
                    print(unichr(intChar))
                if intChar == ord('t'):
                    intChar = ord(u'ั')
                    print(unichr(intChar))
                if intChar == ord('u'):
                    intChar = ord(u'ุ')
                    print(unichr(intChar))
                if intChar == ord('v'):
                    intChar = ord(u'ิ')
                    print(unichr(intChar))
                if intChar == ord('w'):
                    intChar = ord(u'เ')
                    print(unichr(intChar))
                if intChar == ord('x'):
                    intChar = ord(u'ไ')
                    print(unichr(intChar))
                if intChar == ord('y'):
                    intChar = ord(u'์')
                    print(unichr(intChar))
                if intChar == ord('z'):
                    intChar = ord(u'ะ')
                    print(unichr(intChar))
                if intChar == ord('+'):
                    intChar = ord(u'ู')
                    print(unichr(intChar))
                if intChar == ord('!'):
                    intChar = ord(u'ใ')
                    print(unichr(intChar))
                if intChar == ord('*'):
                    intChar = ord(u'ไ')
                    print(unichr(intChar))
                if intChar == ord('/'):
                    intChar = ord(u'า')
                    print(unichr(intChar))
                if intChar == ord(','):
                    intChar = ord(u'แ')
                    print(unichr(intChar))
                if intChar == ord('.'):
                    intChar = ord(u'ี')
                    print(unichr(intChar))
                if intChar == ord(';'):
                    intChar = ord(u'่')
                    print(unichr(intChar))
                if intChar == ord('['):
                    intChar = ord(u'้')
                    print(unichr(intChar))
                if intChar == ord(']'):
                    intChar = ord(u'๊')
                    print(unichr(intChar))
                if intChar == ord('{'):
                    intChar = ord(u'๋')
                    print(unichr(intChar))
                if intChar == ord('}'):
                    intChar = ord(u'ำ')
                    print(unichr(intChar))
                if intChar == ord('#'):
                    intChar = ord(u'ื')
                    print(unichr(intChar))
                if intChar == ord('0'):
                    print(unichr(intChar))
                if intChar == ord('1'):
                    print(chr(intChar))
                if intChar == ord('2'):
                    print(chr(intChar))
                if intChar == ord('3'):
                    print(chr(intChar))
                if intChar == ord('4'):
                    print(chr(intChar))
                if intChar == ord('5'):
                    print(chr(intChar))
                if intChar == ord('6'):
                    print(chr(intChar))
                if intChar == ord('7'):
                    print(chr(intChar))
                if intChar == ord('8'):
                    print(chr(intChar))
                if intChar == ord('9'):
                    print(chr(intChar))





                intClassifications.append(intChar)  # append classification char to integer list of chars (we will convert to float later before writing to file)

                npaFlattenedImage = imgROIResized.reshape((1,
                                                           RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage,
                                               0)  # add current flattened impage numpy array to list of flattened image numpy arrays
            # end if
        # end if
    # end for

    fltClassifications = np.array(intClassifications,
                                  np.float32)  # convert classifications list of ints to numpy array of floats

    npaClassifications = fltClassifications.reshape(
        (fltClassifications.size, 1))  # flatten numpy array of floats to 1d so we can write to file later

    print("\n\ntraining complete !!\n")

    np.savetxt("classifications.txt", npaClassifications)  # write flattened images to file
    np.savetxt("flattened_images.txt", npaFlattenedImages)  #

    cv2.destroyAllWindows()  # remove windows from memory

    return


###################################################################################################
if __name__ == "__main__":
    main()
# end ifad
