import cv2
import numpy as np
from pyzbar.pyzbar import decode

class qrDetector:
    """
    find a qr code in a video and write on the stream the qrCode value
    """

    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # opens webcam , create an instance of VideoCapture
        self.cap.set(3, 640)  # set cap values


    #  draw is boolean --> True for drawing polygon on picture and False for not drawing
    def findQr(self,img,draw):
         polygonCorners={'leftDown' : [], 'leftUp' : [] ,'rightUp' : [] ,'rightDown' : []}  # define a dict which will save 4 corners of the polygon around the qr code
         for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            if draw== True:
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect  # pts2 is for drawing the text straight all the time
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

            for corner in range(4):  # save polygon corners in a dict
                if corner==0:
                    polygonCorners['leftDown']=barcode.polygon[corner]
                if corner==1:
                    polygonCorners['leftUp']=barcode.polygon[corner]
                if corner==2:
                    polygonCorners['rightUp']=barcode.polygon[corner]
                if corner == 3:
                    polygonCorners['rightDown'] = barcode.polygon[corner]

            # print(polygonCorners)  # print the dict values

            return polygonCorners  # return polygon corners dict

    def findRect(self,image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # change the color of the image to gray

        blur = cv2.medianBlur(gray, 5)  # smoothing the image by blurring --> less noise

        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

        thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        min_area = 100
        max_area = 1500
        image_number = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if area > min_area and area < max_area:
                x, y, w, h = cv2.boundingRect(c)
                ROI = image[y:y + h, x:x + w]
                cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
                image_number += 1

        # cv2.imshow('sharpen', sharpen)
        # cv2.imshow('close', close)
        # cv2.imshow('thresh', thresh)
        cv2.imshow('image', image)











