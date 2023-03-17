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
c.execute('''CREATE TABLE IF NOT EXISTS attendance (id REAL, name TEXT,usn TEXT, status TEXT , 
          time TEXT ,n_days REAL,classes_held REAL,percentage REAL)''')

mydata=0
classes_held=10
students=[(1,'Amrutha Bhat','1BM21IS','NULL','NULL',0,classes_held,0),
          (2,'Chaya','1BM21IS049','NULL','NULL',0,classes_held,0),
          (3,'Srushti S Hirematha','1BM21IS181','NULL','NULL',0,classes_held,0),
          (4,'Vinuta S Bhat','1BM21IS204','NULL','NULL',0,classes_held,0),
          (5,'Uditi Singh','1BM21EC189','NULL','NULL',0,classes_held,0)]
c.executemany("INSERT OR REPLACE INTO attendance VALUES(?,?,?,?,?,?,?,?)",students)
print("Reading...")
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
while True:
    success,img=cap.read()
    ret, bw_im = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    for barcode in decode(bw_im):
        
        mydata=barcode.data.decode('utf-8')
    if mydata!=0:
        break
    cv2.imshow('Result',img)
    if mydata==True:
        break
    k=cv2.waitKey(1)
    if k==27:
        break


wer=mydata.strip()
c.execute("SELECT * FROM attendance WHERE usn=?", (mydata.strip(),))
row = c.fetchall()
for tuple in row:
    id,name,usn,status,time,attended,percentage,classes_held=tuple

status = 'present'
attended=int(attended+1)
time = datetime.now().strftime('%H:%M:%S')
classes_held=10
percentage = round((attended / classes_held) * 100, 2)

c.execute('''UPDATE attendance 
    SET status='present',
        time=?,
        n_days=n_days+1,
        classes_held=?,
        percentage=?
    WHERE
        usn=?;
''',(time,classes_held,percentage,wer,))

connection.commit()
connection.close()
cap.release()


my_path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\attendance.db" #Change the path 
my_conn = sqlite3.connect(my_path)
print("Connected to database successfully")
try:
    query="SELECT * FROM attendance" # query to collect record 
    df = pd.read_sql(query,my_conn,index_col='id') # create DataFrame
    
except sqlite3.Error as e:
    
  error = str(e.__dict__['orig'])
  print(error)
else:
  print("DataFrame created successfully..") 
path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\scanner.json"
gc = pygsheets.authorize(service_account_file=path)
sheetname='cnk'
sh=gc.open(sheetname)
wks = sh.worksheet_by_title('std')
wks.clear()
wks.set_dataframe(df,(1,1),copy_index=True,extend=True)  
 
