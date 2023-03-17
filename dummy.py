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
c.execute('CREATE TABLE IF NOT EXISTS attendance (usn TEXT,time TEXT)')

mydata=0
# Get student names and barcodes

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
    if mydata!=0:
        break
    cv2.imshow('Result',img)
    if mydata==True:
        break
    
    k=cv2.waitKey(1)
    if k==27:
        break

# for barcode in decode(bw_im):


print(mydata)
usn=mydata
time = datetime.now().strftime('%H:%M:%S')
c.execute('INSERT INTO attendance ( usn, time) VALUES (?, ?)',(usn,  time))
q=c.fetchall()
print(q)

connection.commit()
connection.close()
cap.release()

my_path="C:\\Users\\Vinuta\\OneDrive\\Documents\\GitHub\\PythonProject-18-03-2023-\\attendance.db" #Change the path 
my_conn = sqlite3.connect(my_path)
print("Connected to database successfully")



try:
    query="SELECT * FROM attendance" # query to collect record 
    df = pd.read_sql(query,my_conn,index_col='usn') # create DataFrame
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
 
