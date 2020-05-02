import cv2
import numpy as np

img = cv2.imread('frame2.png')
img = cv2.line(img,(200,95),(10,410),(0,0,255),5) #center
img = cv2.line(img,(200,145),(545,140),(0,0,255),5) #top
img = cv2.line(img,(55,410),(630,425),(0,0,255),5) #bottom
img = cv2.line(img,(545,140),(630,425),(0,0,255),5) #right

cv2.imwrite('result2.jpg',img)