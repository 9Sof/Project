import cv2
import imutils
import time
import numpy as np

def nothing(x):
    pass
#Box
cv2.namedWindow("Set-Ball") #H สี, S ความอิ่มตัวของสี, V ความเข้มแสง
cv2.createTrackbar("L - H", "Set-Ball", 10, 179, nothing)
cv2.createTrackbar("L - S", "Set-Ball", 80, 255, nothing)
cv2.createTrackbar("L - V", "Set-Ball", 230, 255, nothing)
cv2.createTrackbar("U - H", "Set-Ball", 30, 179, nothing)
cv2.createTrackbar("U - S", "Set-Ball", 255, 255, nothing)
cv2.createTrackbar("U - V", "Set-Ball", 255, 255, nothing)

cap = cv2.VideoCapture(1)
cap1 = cv2.VideoCapture(2)

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

while True:
    ret1, frame1 = cap.read()
    ret2, frame2 = cap1.read()
    ret1, free1 = cap.read()
    ret2, free2 = cap1.read()

#Detect
    ball1 = BallDetect(frame1)
    ball2 = BallDetect(frame2)

#Text
    free1 = cv2.line(free1,(120,164),(3,423),(0,0,255),5)
    free1 = cv2.line(free1,(120,164),(431,168),(0,0,255),5)
    free1 = cv2.line(free1,(3,423),(528,428),(0,0,255),5)
    free1 = cv2.line(free1,(425,120),(570,425),(0,0,255),5)

    free2 = cv2.line(free2,(200,95),(10,410),(0,0,255),5) #center
    free2 = cv2.line(free2,(200,145),(545,140),(0,0,255),5) #top
    free2 = cv2.line(free2,(55,410),(630,425),(0,0,255),5) #bottom
    free2 = cv2.line(free2,(545,140),(630,425),(0,0,255),5) #right

    frame1 = cv2.putText(frame1,"A",(40,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame2 = cv2.putText(frame2,"B",(600,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame1 = cv2.putText(frame1,(str(scoreA)+":"+str(scoreB)),(280,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    frame2 = cv2.putText(frame2,(str(scoreA)+":"+str(scoreB)),(280,50),
        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

 #Count Score
    if ball1 < (100,0): 
        scoreA += 1

    if ball2 > (540,0): 
        scoreB += 1

    cv2.imwrite('frame1.png',frame1)
    cv2.imwrite('frame2.png',frame2)

#Show
    free1 = imutils.resize(free1, width=420)
    free2 = imutils.resize(free2, width=420)
    ball1 = imutils.resize(ball1, width=420)
    ball2 = imutils.resize(ball2, width=420)
    frame1 = imutils.resize(frame1, width=420)
    frame2 = imutils.resize(frame2, width=420)

    cv2.imshow("Free-1", free1)
    cv2.imshow("Free-2", free2)
    cv2.imshow("Ball-1", ball1)
    cv2.imshow("Ball-2", ball2)
    cv2.imshow("Frame-1", frame1)
    cv2.imshow("Frame-2", frame2)
    
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()
        