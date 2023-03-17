import cv2
import pyzbar.pyzbar as pyzbar
import time
from datetime import datetime
import pandas as pd

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
a=0
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
names=[]
fob=open('attendance.txt','a+')
print('reading code...')
while True:
    _,frame=cap.read()
    ret, bw_im = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    decode=pyzbar.decode(frame)
    for obj in decode:
        a=obj.data.decode('utf-8')
        a.strip()
        fob.write(a+","+current_time)
        time.sleep(1)
    cv2.imshow('Result',frame)
    if cv2.waitKey(1)==1 or a!=0:
        cv2.destroyAllWindows()
        break
# opening and creating new .txt file
with open("attendance.txt", 'r') as r:
    for line in r:
        line.strip()
            
fob.close()
df = pd.read_csv('attendance.txt') # can replace with df = pd.read_table('input.txt') for '\t'
df.to_excel('output.xlsx', 'Sheet1')

