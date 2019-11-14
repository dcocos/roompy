import cv2
import numpy as np

cap = cv2.VideoCapture(0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

while True:
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=5)

    cv2.imshow('frame', fgmask)

    n_white_pix = np.sum(fgmask == 255)

    n_total_pix = fgmask.size

    print(n_total_pix)

    print(n_white_pix / n_total_pix)

    if n_white_pix / n_total_pix > 0.01 * n_total_pix:
        print("Movement detected")

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
