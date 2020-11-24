#importing libraries
import cv2 as cv
import numpy as np
from time import *

t = ctime(time())
t = t.split()
img = np.zeros((400,400,3))

def day(d):
    d = d.lower()
    if d=='sun':
        return 'Sunday'
    elif d=='mon':
        return 'Monday'
    elif d=='tue':
        return 'Tuesday'
    elif d=='wed':
        return 'Wednesday'
    elif d=='thu':
        return 'Thursday'
    elif d=='fri':
        return 'Friday'
    elif d=='sat':
        return 'Saturday'

t1 = time()
while True:
    if time()-t1>5:
        break
    t = ctime(time())
    t = t.split()
    img = cv.imread("sky.jpg")
    img = cv.resize(img,(400,300))
    img = cv.putText(img,str(t[3]),(50,150),cv.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5,cv.LINE_AA)
    img = cv.putText(img,str(t[1])+"  "+str(t[2])+"  "+str(t[4]),(70,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3,cv.LINE_AA)
    d = day(t[0])
    img = cv.putText(img,d,(135,200),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3,cv.LINE_AA)
    
    cv.imshow('DeskClock',img)
    cv.waitKey(1)
cv.destroyAllWindows()


