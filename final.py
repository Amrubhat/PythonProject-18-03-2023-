import cv2
from pyzbar.pyzbar import decode
import sqlite3
from datetime import datetime
import sqlite3
import pandas as pd
import pygsheets

#connecting database
connection = sqlite3.connect('attendance.db')
c = connection.cursor()

eligibility="ineligible"
mydata=0
classes_held=5

print("Reading...")

#start webcam
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

#scanning barcode
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

#removing spaces and fetching data
wer=mydata.strip()
c.execute("SELECT * FROM attendance WHERE usn=?", (mydata.strip(),))
row = c.fetchall()
for tuple in row:
    id,name,usn,status,time,attended,percentage,classes_held,eligibility=tuple

status = 'present'
attended=int(attended+1)

#record time
time = datetime.now().strftime('%H:%M:%S')
classes_held=5

#calculation of attendance and checking eligibility
percentage = round((attended / classes_held) * 100, 2)
if percentage>=85:
    eligibility="eligible"

#updating data to database
if attended<=classes_held:
    c.execute('''UPDATE attendance 
        SET status='present',
            time=?,
            attended=?,
            classes_held=?,
            percentage=?,
            eligibility=?
        WHERE
            usn=?;
    ''',(time,attended,classes_held,percentage,eligibility,wer,))
    print("Marked present")
else:
    print("Last working day of current semester is over")


connection.commit()
connection.close()
cap.release()

#connecting database to google sheets
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
wks = sh.worksheet_by_title('19_Mar')
wks.clear()
wks.set_dataframe(df,(1,1),copy_index=True,extend=True)  
 