import cv2
from pyzbar.pyzbar import decode
import numpy as np
import sqlite3
from datetime import datetime
import sqlite3
import pandas as pd
import pygsheets

connection = sqlite3.connect('attendance.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS attendance (id REAL, name TEXT,usn TEXT, status TEXT , time TEXT ,n_days REAL)')

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
    if mydata!=0:
        break
    cv2.imshow('Result',img)
    if mydata==True:
        break
    
    k=cv2.waitKey(1)
    if k==27:
        break
print("out of while loop")
print(mydata)
c.execute("SELECT * FROM attendance WHERE usn=?", ('1BM21IS181',))
row = c.fetchall()
print(row)
# for barcode in decode(bw_im):
for tuple in row:
    id,name,usn,status,time,n_days=tuple
    print(name,usn)
    print(mydata)

print(usn)
status = 'present'
n_days=+1
time = datetime.now().strftime('%H:%M:%S')
c.execute('INSERT INTO attendance ( status, time, n_days) VALUES (?, ?, ?)',(status,  time,n_days))
print(name + ' is present.')
print(n_days)
total_classes=5
percentage = round((n_days / total_classes) * 100, 2)
print(f'{name}: {percentage}%')


connection.commit()
connection.close()

cap.release()

my_path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\barcode.py" #Change the path 
my_conn = sqlite3.connect(my_path)
print("Connected to database successfully")



try:
    query="SELECT * FROM attendance" # query to collect record 
    df = pd.read_sql(query,my_conn,index_col='id') # create DataFrame
    print(df.head(4))
except sqlite3.Error as e:
    #print(e)
  error = str(e.__dict__['orig'])
  print(error)
else:
  print("DataFrame created successfully..") 

path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\scanner.json"
gc = pygsheets.authorize(service_account_file=path)
sheetname='cnk'
sh=gc.open(sheetname)
wks = sh.worksheet_by_title('std')

# wks.update_value('A1',42)
# wks.update_value('A2',45)

# print('done')
wks.clear()
wks.set_dataframe(df,(1,1),copy_index=True,extend=True)  
 
