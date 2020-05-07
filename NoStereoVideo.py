import cv2
import imutils
import time
import numpy as np

#CreateBox
def nothing(x):
    pass
cv2.namedWindow("Set-Ball") #H สี, S ความอิ่มตัวของสี, V ความเข้มแสง
cv2.createTrackbar("L - H", "Set-Ball", 130, 255, nothing)
cv2.createTrackbar("L - S", "Set-Ball", 60, 255, nothing)
cv2.createTrackbar("L - V", "Set-Ball", 130, 255, nothing)
cv2.createTrackbar("U - H", "Set-Ball", 170, 255, nothing)
cv2.createTrackbar("U - S", "Set-Ball", 225, 255, nothing)
cv2.createTrackbar("U - V", "Set-Ball", 225, 255, nothing)

scoreA = 0
scoreB = 0

cap = cv2.VideoCapture('PingpongCrop2_1.mp4')
cap1 = cv2.VideoCapture('Pingpong.mp4')

while True:
    ret, frame = cap.read()
    ret, freeframe = cap1.read()
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
    res = cv2.bitwise_and(freeframe,frame, mask=mask)

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
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
###################################
#score
        if scoreA != 10 and scoreB != 10 :
            if center:

                while j>=10:
                    ret, frame = cap.read()
                    ret, freeframe = cap1.read()
    ###################################
    #Text               
                    freeframe = cv2.putText(freeframe,"A",(100,100),
                        cv2.FONT_HERSHEY_SIMPLEX,5,(0,0,255),10)
                    freeframe = cv2.putText(freeframe,"B",(1820,100),
                        cv2.FONT_HERSHEY_SIMPLEX,5,(0,0,255),10)
                    freeframe = cv2.putText(freeframe,(str(scoreA)+":"+str(scoreB)),(910,100),
                        cv2.FONT_HERSHEY_SIMPLEX,5,(0,0,255),10)

                    freeframe = cv2.line(freeframe,(700,1080),(990,570),(0,0,255),5) #center
                    freeframe = cv2.line(freeframe,(212,710),(1645,740),(0,0,255),8) #bottom
                    freeframe = cv2.line(freeframe,(212,710),(490,565),(0,0,255),8) #left
                    freeframe = cv2.line(freeframe,(1645,740),(1483,578),(0,0,255),8) #right

                    freeframe = imutils.resize(freeframe, width=420)
                    cv2.imshow('Ball in the game',freeframe)

                    if j%10 == 0:
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(freeframe,str(j//10),(250,250), font, 10,(255,255,255),10,cv2.LINE_AA)
                    freeframe = imutils.resize(freeframe, width=420)
                    cv2.imshow('Countdown',freeframe)
                    cv2.waitKey(125)
                    j = j-1
                    if center[0] > 212 and center[0] < 1645: 
                       break
                    print('j after :',j)
                else:
                    if center[0] < 212 and center[1] > 710 and center[0] < 490 and center[1] > 565: 
                        scoreA += 1
                        print('scoreA')
                        print(center[0],' : ',center[1])
                    # elif center[0] < 340 and center[1] > 380: 
                    #     scoreA += 1
                    #     print('scoreA')
                            
                    # elif center[0] > 540: 
                    #     scoreB += 1
                    # elif center[0] > 340 and center[1] > 380: 
                    #     scoreB += 1

        else:
            scoreA = 0
            scoreB = 0  

########################################
#Show    
    res = imutils.resize(res, width=420)  
    cv2.imshow("Ball",res)
    if k == ord("q"):
	    break

cap.release()  
cv2.destroyAllWindows()