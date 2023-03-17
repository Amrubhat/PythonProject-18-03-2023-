import cv2
from pyzbar.pyzbar import decode
import numpy as np
import sqlite3
from datetime import datetime

connection = sqlite3.connect('attendance.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,usn TEXT, status TEXT NOT NULL, time TEXT NOT NULL,n_days INTEGER)')

mydata=0
# Get student names and barcodes
students=[('1','vinuta','1BM21IS204','NULL','NULL','NULL'),('2','srushti','1BM21IS181','NULL','NULL','NULL')]
c.executemany("INSERT OR REPLACE INTO attendance VALUES(?,?,?,?,?,?)",students)
# c.execute("SELECT * FROM attendance")
# item=c.fetchall()
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
   
    success,img=cap.read()
    ret, bw_im = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
       
       # zbar
   
    for barcode in decode(bw_im):
        print(barcode.data)
        mydata=barcode.data.decode('utf-8')
        print(mydata)
        # pts=np.array([barcode.polygon],np.int32)
        # pts=pts.reshape((-1,1,2))
        # cv2.polylines(bw_im,[pts],True,(255,0,255),5)
        # pts2=barcode.rect
        # cv2.putText(bw_im,mydata,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_COMPLEX,0.9,(2550,   255),4)

    cv2.imshow('Result',img)
    if mydata==True:
        break
    
    k=cv2.waitKey(1)
    if k==27:
        break
    print(mydata)
    c.execute("SELECT * FROM attendance WHERE usn=?", (mydata,))
    row = c.fetchone()
    print(row)
# i=0
# # for barcode in decode(bw_im):
# for i in row:
#     name,usn,status,time=i
#     if mydata == usn:
#         status = 'present'
#         n_days=+1
#         time = datetime.date.today().strftime('%H:%M:%S')
#         c.execute('INSERT INTO attendance (name, status, date) VALUES (?, ?, ?)',(status, time,n_days))
#         print(name + ' is present.')
#         break
    
# for i in row:
#     name,usn,status,time,n_days=i
#     total_classes=5
#     percentage = round((n_days / total_classes) * 100, 2)
#     print(f'{name}: {percentage}%')

connection.commit()
connection.close()

cap.release()
cv2.destroyAllWindows()
 
