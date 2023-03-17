import sqlite3
import datetime
import pyzbar.pyzbar as pyzbar
import cv2

# Connect to the database
conn = sqlite3.connect('attendance.db')

# Create a table for storing attendance
conn.execute('CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, status TEXT NOT NULL, date TEXT NOT NULL)')

# Get student names and barcodes
students = []
while True:
    name = input('Enter student name (enter "done" to finish): ')
    if name == 'done':
        break
    barcode = input('Enter barcode for ' + name + ': ')
    students.append((name, barcode))

# Initialize video capture
cap = cv2.VideoCapture(0)

# Define barcode scanning function
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 1.0, (255, 255, 255), 1)
    return frame

# Take attendance
while True:
    ret, frame = cap.read()
    frame = read_barcodes(frame)
    cv2.imshow('Barcode Scanner', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        for name, student_barcode in students:
            if barcode_info == student_barcode:
                status = 'present'
                date = datetime.date.today().strftime('%Y-%m-%d')
                conn.execute('INSERT INTO attendance (name, status, date) VALUES (?, ?, ?)', (name, status, date))
                print(name + ' is present.')
                break

# Calculate percentage attendance
for name, _ in students:
    cursor = conn.execute('SELECT COUNT(*) FROM attendance WHERE name = ? AND status = ?', (name, 'present'))
    total_present = cursor.fetchone()[0]
    cursor = conn.execute('SELECT COUNT(*) FROM attendance WHERE name = ?', (name,))
    #total_classes = cursor.fetchone()[0]
    total_classes=3

    percentage = round((total_present / total_classes) * 100, 2)
    print(f'{name}: {percentage}%')

# Close the database connection
conn.commit()
conn.close()

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()