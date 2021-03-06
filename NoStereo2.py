import cv2
import imutils
import time
import numpy as np

#CreateBox
def nothing(x):
    pass
cv2.namedWindow("Set-Color")
cv2.createTrackbar("Low-H", "Set-Color", 20, 179, nothing) #10
cv2.createTrackbar("Low-S", "Set-Color", 80, 255, nothing)
cv2.createTrackbar("Low-V", "Set-Color", 180, 255, nothing) #160
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

    frameL = cv2.line(frameL,(100,100),(100,380),(0,0,255),5)
    frameL = cv2.line(frameL,(540,100),(540,380),(0,0,255),5)
    frameL = cv2.line(frameL,(100,380),(540,380),(0,0,255),5)
    frameL = cv2.line(frameL,(340,0),(340,480),(0,0,255),5)

###################################
#Text
    frameL = cv2.putText(frameL,"A",(40,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frameL = cv2.putText(frameL,"B",(600,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frameL = cv2.putText(frameL,(str(scoreA)+":"+str(scoreB)),(280,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
###################################
#Score
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
        
        if center[0] < 100: 
            scoreA += 1
        elif center[0] < 340 and center[1] > 380: 
            scoreA += 1
        
        elif center[0] > 100 and center[0] < 540 and center[1] < 380:
            print('Feild')
            print(center[0],' : ',center[1])
        elif center[0] > 540: 
            scoreB += 1
        elif center[0] > 340 and center[1] > 380: 
            scoreB += 1
            print(center[0],' : ',center[1])

########################################
#Show
    frame = imutils.resize(frame, width=420)
    mask = imutils.resize(mask, width=420)
    res = imutils.resize(res, width=420)
    frameL = imutils.resize(frameL, width=420)

    cv2.imshow("Score",frameL)
    cv2.imshow("Frame",frame)
    cv2.imshow("Ball",mask)
    cv2.imshow("Res",res)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()