import cv2
import numpy as np

from utils.Event import Event


class Detector:

    def __init__(self):
        self.motionDetected = Event()
        self.cap = cv2.VideoCapture(0)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

    def fire(self):
        while True:
            ret, frame = self.cap.read()
            fgmask = self.fgbg.apply(frame)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel, iterations=5)

            cv2.imshow('frame', fgmask)

            n_white_pix = np.sum(fgmask == 255)
            n_total_pix = fgmask.size
            white_percent = n_white_pix / float(n_total_pix)
            threshold = 0.02

            print("n_white_pix: %s , n_total_pix: %s, white_percent: %s, threshold: %s" % (
                n_white_pix, n_total_pix, white_percent, threshold))
            if white_percent > threshold:
                print("Movement detected")
                self.motionDetected()

            key = cv2.waitKey(1) & 0xFF
            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
