import cv2
import numpy as np
import imutils

def nothing(x):
    pass
#Box
cv2.namedWindow("Set-Ball") #H สี, S ความอิ่มตัวของสี, V ความเข้มแสง
cv2.createTrackbar("L - H", "Set-Ball",130, 255, nothing)
cv2.createTrackbar("L - S", "Set-Ball", 60, 255, nothing)
cv2.createTrackbar("L - V", "Set-Ball", 130, 255, nothing)
cv2.createTrackbar("U - H", "Set-Ball", 170, 255, nothing)
cv2.createTrackbar("U - S", "Set-Ball", 180, 255, nothing)
cv2.createTrackbar("U - V", "Set-Ball", 200, 255, nothing)

img = cv2.imread('frame1.png')


while (1):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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
    res = cv2.bitwise_and(img,img, mask=mask)
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
            cv2.circle(img, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(img, center, 3, (0, 0, 255), -1)


    img = cv2.line(img,(700,1080),(990,570),(0,0,255),5) #center
    img = cv2.line(img,(212,710),(1645,740),(0,0,255),8) #bottom
    img = cv2.line(img,(212,710),(490,565),(0,0,255),8) #left
    img = cv2.line(img,(1645,740),(1483,578),(0,0,255),8) #right

    # img = imutils.resize(img, width=420)
    cv2.imshow('result2',img)
    cv2.imshow("mask", mask)
    cv2.imshow("result", res)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
	    break

img.release()  
cv2.destroyAllWindows()