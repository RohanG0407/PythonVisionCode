import cv2
import numpy as np
frame = cv2.imread('test.JPG')

while(True):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([85,100,250])
    upper_green = np.array([95,200,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame,frame,mask=mask)
    #cv2.imshow('orig',frame)
    cv2.imshow('fff',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    def onmouse(k,x,y,s,p):
        global hsv
        if k==1:   # left mouse, print pixel at x,y
            print hsv[y,x]

    cv2.namedWindow("hsv")
    cv2.setMouseCallback("hsv",onmouse);
    cv2.imshow('hsv',hsv)
vid.release()
cv2.destroyAllWindows()