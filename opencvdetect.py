import argparse
import datetime
import json
import time
import warnings

import cv2
import imutils

cap = cv2.VideoCapture(0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

while (1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=5)

    cv2.imshow('frame', fgmask)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()