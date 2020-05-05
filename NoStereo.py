import cv2
import imutils
import time
import numpy as np

#CreateBox
def nothing(x):
    pass
cv2.namedWindow("Set-Color")
cv2.createTrackbar("Low-H", "Set-Color", 10, 179, nothing)
cv2.createTrackbar("Low-S", "Set-Color", 80, 255, nothing)
cv2.createTrackbar("Low-V", "Set-Color", 160, 255, nothing)
cv2.createTrackbar("Up-H", "Set-Color", 30, 179, nothing)
cv2.createTrackbar("Up-S", "Set-Color", 255, 255, nothing)
cv2.createTrackbar("Up-V", "Set-Color", 255, 255, nothing)

scoreA = 0
scoreB = 0

cap = cv2.VideoCapture(1)
#cap2 = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    ret, frameL = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("Low-H", "Set-Color")
    l_s = cv2.getTrackbarPos("Low-S", "Set-Color")
    l_v = cv2.getTrackbarPos("Low-V", "Set-Color")
    u_h = cv2.getTrackbarPos("Up-H", "Set-Color")
    u_s = cv2.getTrackbarPos("Up-S", "Set-Color")
    u_v = cv2.getTrackbarPos("Up-V", "Set-Color")
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    frame = cv2.line(frame,(100,0),(100,480),(0,0,255),5)
    frame = cv2.line(frame,(540,0),(540,480),(0,0,255),5)

###################################
#Text
    frame = cv2.putText(frame,"A",(40,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame = cv2.putText(frame,"B",(600,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame = cv2.putText(frame,(str(scoreA)+":"+str(scoreB)),(280,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
###################################
#ball tracking

    frame = imutils.resize(frame, width=420)
    cv2.imshow('0',frame)
    k = cv2.waitKey(1)    
    j = 30

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        if radius > 2.5:
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
###################################
#score
        if center:
            while j>=10:
                ret, frame = cap.read()

                if j%10 == 0:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,str(j//10),(250,250), font, 7,(255,255,255),10,cv2.LINE_AA)
                frame = imutils.resize(frame, width=420)
                cv2.imshow('1',frame)
                cv2.waitKey(125)
                j = j-1
            else:
                ret, frame = cap.read()
               
                if center < (100,0) and center < (100,480) : 
                    scoreA += 1

                elif center > (540,0) and center > (540,480) : 
                    scoreB += 1
                frame = imutils.resize(frame, width=420)
                cv2.imshow('set',frame)

########################################
#Show
    res = imutils.resize(res, width=420)
    frame = imutils.resize(frame, width=420)
    
    cv2.imshow("Score",frame)
    cv2.imshow("Ball",res)


    if k == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()