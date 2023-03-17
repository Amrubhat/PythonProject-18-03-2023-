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
          time TEXT ,attended REAL,classes_held REAL,percentage REAL,eligibility TEXT)''')

mydata=0
classes_held=5
eligibility="ineligible"
students=[(1,'Amrutha Bhat','1BM21IS','NULL','NULL',0,classes_held,0,'ineligible'),
          (2,'Chaya','1BM21IS049','NULL','NULL',0,classes_held,0,'ineligible'),
          (3,'Srushti S Hirematha','1BM21IS181','NULL','NULL',0,classes_held,0,'ineligible'),
          (4,'Vinuta S Bhat','1BM21IS204','NULL','NULL',0,classes_held,0,'ineligible'),
          (5,'Uditi Singh','1BM21EC189','NULL','NULL',0,classes_held,0,'ineligible')]
c.executemany("INSERT OR REPLACE INTO attendance VALUES(?,?,?,?,?,?,?,?,?)",students)

connection.commit()
connection.close()