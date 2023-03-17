
from pyzbar.pyzbar import decode

import sqlite3

import sqlite3


connection = sqlite3.connect('attendance.db')
c = connection.cursor()
c.execute("DROP TABLE attendance")

