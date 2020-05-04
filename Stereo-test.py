import cv2
import imutils
import time
import numpy as np

def nothing(x):
    pass
#Boxq
cv2.namedWindow("Set-Ball") #H สี, S ความอิ่มตัวของสี, V ความเข้มแสง
cv2.createTrackbar("L - H", "Set-Ball",20, 255, nothing)
cv2.createTrackbar("L - S", "Set-Ball", 0, 255, nothing)
cv2.createTrackbar("L - V", "Set-Ball", 0, 255, nothing)
cv2.createTrackbar("U - H", "Set-Ball", 200, 255, nothing)
cv2.createTrackbar("U - S", "Set-Ball", 240, 255, nothing)
cv2.createTrackbar("U - V", "Set-Ball", 240, 255, nothing)



cap = cv2.VideoCapture('PingpongCrop2.mp4')

scoreA = 0
scoreB = 0


def BallDetect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Set-Ball")
    l_s = cv2.getTrackbarPos("L - S", "Set-Ball")
    l_v = cv2.getTrackbarPos("L - V", "Set-Ball")
    u_h = cv2.getTrackbarPos("U - H", "Set-Ball")
    u_s = cv2.getTrackbarPos("U - S", "Set-Ball")
    u_v = cv2.getTrackbarPos("U - V", "Set-Ball")
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask=mask)
    ###################################
    #BallDetect
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
    return res

def BallDetect1(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Set-Ball")
    l_s = cv2.getTrackbarPos("L - S", "Set-Ball")
    l_v = cv2.getTrackbarPos("L - V", "Set-Ball")
    u_h = cv2.getTrackbarPos("U - H", "Set-Ball")
    u_s = cv2.getTrackbarPos("U - S", "Set-Ball")
    u_v = cv2.getTrackbarPos("U - V", "Set-Ball")
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask=mask)
    ###################################
    #BallDetect
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

        if center < (100,0) and center < (100,480) : 
            scoreA += 1

    return scoreA

def BallDetect2(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Set-Ball")
    l_s = cv2.getTrackbarPos("L - S", "Set-Ball")
    l_v = cv2.getTrackbarPos("L - V", "Set-Ball")
    u_h = cv2.getTrackbarPos("U - H", "Set-Ball")
    u_s = cv2.getTrackbarPos("U - S", "Set-Ball")
    u_v = cv2.getTrackbarPos("U - V", "Set-Ball")
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame,frame, mask=mask)
    ###################################
    #BallDetect
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
    return center
while True:
    ret1, frame1 = cap.read()
    ret1, free1 = cap.read()

#Detect
    ball1 = BallDetect(frame1)

    

#Text
    frame1 = cv2.line(frame1,(200,95),(10,410),(0,0,255),5) #center
    frame1 = cv2.line(frame1,(212,710),(1645,740),(0,0,255),8) #bottom
    frame1 = cv2.line(frame1,(212,710),(490,565),(0,0,255),8) #left
    frame1 = cv2.line(frame1,(1645,740),(1483,578),(0,0,255),8) #right


    frame1 = cv2.putText(frame1,"A",(40,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame1 = cv2.putText(frame1,(str(scoreA)+":"+str(scoreB)),(280,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)


    cv2.imwrite('frame1.png',frame1)

#Show
    free1 = imutils.resize(free1, width=420)
    ball1 = imutils.resize(ball1, width=420)
    frame1 = imutils.resize(frame1, width=420)

    cv2.imshow("Free-1", free1)
    cv2.imshow("Ball-1", ball1)
    cv2.imshow("Frame-1", frame1)
    
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()
        