
import cv2

import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows= False)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = fgbg.apply(frame)


    cv2.imshow("Frame", frame)
    cv2.imshow("FG Mask Frame", fgmask)

    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard ==27:
        break

cap.release()
cap.destroyAllWindows()
