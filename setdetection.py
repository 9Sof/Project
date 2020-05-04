import cv2
import numpy as np
#7-93-200,26-246-255
def nothing(x):
    pass
cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("Low-H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("Low-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Low-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Up-H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("Up-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Up-V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("Low-H", "Trackbars")
    l_s = cv2.getTrackbarPos("Low-S", "Trackbars")
    l_v = cv2.getTrackbarPos("Low-V", "Trackbars")
    u_h = cv2.getTrackbarPos("Up-H", "Trackbars")
    u_s = cv2.getTrackbarPos("Up-S", "Trackbars")
    u_v = cv2.getTrackbarPos("Up-V", "Trackbars")
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()