import cv2
from pyzbar.pyzbar import decode
import numpy as np
import re
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
mydata=0
a=0
while True:
    success,img=cap.read()
    ret, bw_im = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # zbar
   
    for barcode in decode(bw_im):
        mydata=barcode.data.decode('utf-8')
        pts=np.array([barcode.polygon],np.int32)
        pts=pts.reshape((-1,1,2))
        cv2.polylines(bw_im,[pts],True,(255,0,255),5)
        pts2=barcode.rect
        cv2.putText(bw_im,mydata,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255),4)
        
    cv2.imshow('Result',img)
    if mydata!=0:
        print(mydata)
        break
    # if mydata=="1BM21IS204":
    #     break
       
    cv2.waitKey(1) 

    