import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    canny = cv2.Canny(blur, 150, 255, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

    # Find Vertical Lines
    # ------ 
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))
    remove_horizontal = cv2.morphologyEx(canny, cv2.MORPH_OPEN, vertical_kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    dilate_vertical = cv2.morphologyEx(remove_horizontal, cv2.MORPH_CLOSE, kernel, iterations=5)

    minLineLength = 5
    maxLineGap = 20
    mask = np.zeros(frame.shape, np.uint8)
    lines = cv2.HoughLinesP(dilate_vertical,1,np.pi/180,100,minLineLength,maxLineGap)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(mask,(x1,y1),(x2,y2),(255,255,255),3)
    mask = imutils.resize(mask, width=300)
    cv2.imshow('vertical_mask', mask)
    # ------ 

    # Find Horizontal Lines
    # ------ 
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,1))
    remove_vertical = cv2.morphologyEx(canny, cv2.MORPH_OPEN, horizontal_kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilate_horizontal = cv2.morphologyEx(remove_vertical, cv2.MORPH_CLOSE, kernel, iterations=3)

    minLineLength = 5
    maxLineGap = 20
    horizontal_mask = np.zeros(frame.shape, np.uint8)
    lines = cv2.HoughLinesP(dilate_horizontal,1,np.pi/180,100,minLineLength,maxLineGap)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(mask,(x1,y1),(x2,y2),(255,255,255),3)
            cv2.line(horizontal_mask,(x1,y1),(x2,y2),(255,255,255),3)
    horizontal_mask = imutils.resize(horizontal_mask, width=300)
    cv2.imshow('horizontal_mask', horizontal_mask)
    # ------ 

    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(frame, [c], -1, (36,255,12), 2)

    remove_vertical = imutils.resize(remove_vertical, width=300)
    remove_horizontal = imutils.resize(remove_horizontal, width=300)
    dilate_horizontal = imutils.resize(dilate_horizontal, width=300)
    mask = imutils.resize(mask, width=300)
    frame = imutils.resize(frame, width=300)
    
    cv2.imshow('remove_vertical', remove_vertical)
    cv2.imshow('remove_horizontal', remove_horizontal)
    cv2.imshow('dilate_horizontal', dilate_horizontal)
    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	    break
cv2.destroyAllWindows()