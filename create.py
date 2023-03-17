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
students=[(1,'vinuta','1BM21IS204','NULL','NULL',0),(2,'srushti','1BM21IS181','NULL','NULL',0)]
c.executemany("INSERT OR REPLACE INTO attendance VALUES(?,?,?,?,?,?)",students)
# c.execute("SELECT * FROM attendance")
# item=c.fetchall()


connection.commit()
connection.close()



