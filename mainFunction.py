import main
import cv2
import numpy as np
from pyzbar.pyzbar import decode
def detectQrMain():
    itay = main.qrDetector()  #create a new instance of qrDetector
    cap = itay.cap  # save attribute cap from object
    while True:  # iterate the webcam video stream2
        success, img = cap.read()  # read each image from stream --> save the current frame in 'img'
        itay.findRect(img)
        polygonCornersDict=itay.findQr(img,False)  # find the qrCode in the given image
        if polygonCornersDict is not None:
            print(polygonCornersDict)
        # if polygonCornersDict!=None:
        #     print(polygonCornersDict.get('image'))
        cv2.imshow('Result', img)  # show image to screen
        cv2.waitKey(1)  # stop occur by the user




detectQrMain()