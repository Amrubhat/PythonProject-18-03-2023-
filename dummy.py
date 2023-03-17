import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import sys
import time
import pybase64
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

a=0
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
names=[]
fob=open('attendance.txt','a+')
# def enterdata(z):
#     if z in names:
#         pass
#     else:
#         names.append(z)
#         z=".join(str(z))"
#         fob.write(z+'\n')
#         return names
print('reading code...')

# def checkdata(data):
#     data=str(data)
#     if data in names:
#         print('Already present')
#     else:
#         print(data+'Marked present')
#         enterdata(data)
#     return 1

while True:
    
    _,frame=cap.read()
    ret, bw_im = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    decode=pyzbar.decode(frame)
    for obj in decode:
        a=obj.data.decode('utf-8')
        fob.write(a+current_time+'\n')
        # mydata=obj.data.decode('utf-8')
        # pts=np.array([obj.polygon],np.int32)
        # pts=pts.reshape((-1,1,2))
        # cv2.polylines(bw_im,[pts],True,(255,0,255),5)
        # pts2=obj.rect
        # cv2.putText(bw_im,decode,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,0,255),4)
        time.sleep(1)
    cv2.imshow('Result',frame)
    if cv2.waitKey(1)==1 or a!=0:
        cv2.destroyAllWindows()
        break
fob.close()

