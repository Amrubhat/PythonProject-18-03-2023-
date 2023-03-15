import cv2

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)



# img = cv2.imread(img_fn,cv2.IMREAD_GRAYSCALE)
# ret, bw_im = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
# barcodes = pyzbar.decode(bw_im, symbols=[ZBarSymbol.QRCODE])
# camera=True
# while camera==True:
#     success,frame=cap.read()
#     for code in decode(frame):
#         print(code.type)
#         print(code.data.decode('utf-8'))
#     cv2.imshow('Testing-code-scan',frame)
#     cv2.waitKey(1)
while True:
    success,img=cap.read()


    for barcode in decode(img):
        print(barcode.data)
        mydata=barcode.data.decode('utf-8')
        print(mydata)
    cv2.imshow('Result',img)
    cv2.waitKey(1)