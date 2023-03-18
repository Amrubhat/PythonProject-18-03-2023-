import sqlite3
import cv2
from pyzbar.pyzbar import decode

# Initialize database connection
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Create products table
c.execute('''CREATE TABLE products
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              barcode TEXT)''')

# Initialize video capture
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
    
decoded_objects=barcode.data
while True:
    # Capture frame from video stream
    ret, frame = cap.read()

    # Decode barcode from frame
    decoded_objects = decode(frame)

    # Iterate through decoded objects
    for obj in decoded_objects:
        # Check if barcode already exists in database
        c.execute("SELECT * FROM products WHERE barcode=?", (obj.data.decode('utf-8'),))
        row = c.fetchone()

        # If barcode doesn't exist, add product to database
        if row is None:
            name = input('Enter product name: ')
            barcode = obj.data.decode('utf-8')
            c.execute("INSERT INTO products (name, barcode) VALUES (?, ?)", (name, barcode))
            conn.commit()

    # Show video stream
    cv2.imshow('Barcode Scanner', frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close database connection
conn.close()

# Release video capture and destroy windows
cap.release()
cv2.destroyAllWindows()