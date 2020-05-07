import cv2
import imutils
import time
import numpy as np

#CreateBox
def nothing(x):
    pass
cv2.namedWindow("Set-Ball") #H สี, S ความอิ่มตัวของสี, V ความเข้มแสง
cv2.createTrackbar("L - H", "Set-Ball", 10, 179, nothing)
cv2.createTrackbar("L - S", "Set-Ball", 120, 255, nothing)
cv2.createTrackbar("L - V", "Set-Ball", 230, 255, nothing)
cv2.createTrackbar("U - H", "Set-Ball", 30, 179, nothing)
cv2.createTrackbar("U - S", "Set-Ball", 255, 255, nothing)
cv2.createTrackbar("U - V", "Set-Ball", 255, 255, nothing)

scoreA = 0
scoreB = 0

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    ret, freeframe = cap.read()

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
#ball tracking
    k = cv2.waitKey(125)    
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
            cv2.circle(freeframe, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(freeframe, center, 3, (0, 0, 255), -1)
###################################
#score
        if scoreA != 5 and scoreB != 5 :
            if center:

                while j>=10:
                    ret, frame = cap.read()
    ###################################
    #Text               
                    frame = cv2.putText(frame,"A",(40,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                    frame = cv2.putText(frame,"B",(600,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                    frame = cv2.putText(frame,(str(scoreA)+":"+str(scoreB)),(280,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                    frame = cv2.line(frame,(100,100),(100,380),(0,0,255),5)
                    frame = cv2.line(frame,(540,100),(540,380),(0,0,255),5)
                    frame = cv2.line(frame,(100,380),(540,380),(0,0,255),5)
                    frame = cv2.line(frame,(340,0),(340,480),(0,0,255),5)

                    frame = imutils.resize(frame, width=420)
                    cv2.imshow('Ball in the game',frame)

                    if j%10 == 0:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,str(j//10),(250,250), font, 7,(255,255,255),10,cv2.LINE_AA)
                    frame = imutils.resize(frame, width=420)
                    cv2.imshow('Countdown',frame)
                    cv2.waitKey(125)
                    j = j-1
                    if center[0] > 100 and center[0] < 540 and center[1] < 380: 
                       break
                    print('j after :',j)
                else:
                    if center[0] < 100: 
                        scoreA += 1
                        print('scoreA')
                        print(center[0],' : ',center[1])
                    elif center[0] > 100 and center[0] < 540 and center[1] < 380:
                        print('Feild')
                    elif center[0] < 340 and center[1] > 380: 
                        scoreA += 1
                        print('scoreA')
                            
                    elif center[0] > 540: 
                        scoreB += 1
                    elif center[0] > 340 and center[1] > 380: 
                        scoreB += 1

        else:
            scoreA = 0
            scoreB = 0  

########################################
#Show
    print(center[0],' a:a ',center[1])    
    res = imutils.resize(res, width=420)  
    freeframe = imutils.resize(freeframe, width=420)
    cv2.imshow('freeframe',freeframe)
    cv2.imshow("Ball",res)


    if k == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()