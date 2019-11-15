import cv2
import numpy as np

from utils.Event import Event


class Eyes:

    def __init__(self, show: bool):
        self.show = show
        self.motionDetected = Event()
        self.panicDetected = Event()
        self.cap = cv2.VideoCapture(0)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
        self.frame_count = 0

    def detect(self):
        try:
            while True:
                ret, frame = self.cap.read()
                fgmask = self.fgbg.apply(frame)
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel, iterations=5)

                if self.show:
                    cv2.imshow('frame', fgmask)

                n_white_pix = np.sum(fgmask == 255)
                n_total_pix = fgmask.size
                white_percent = n_white_pix / float(n_total_pix)
                threshold = 0.02

                if 100 < self.frame_count:
                    if white_percent > threshold:
                        self.motionDetected()

                self.detect_panic(white_percent)

                key = cv2.waitKey(1) & 0xFF
                # if the `q` key is pressed, break from the loop
                if key == ord("q"):
                    break

                self.frame_count += 1
        finally:
            self.cap.release()
            cv2.destroyAllWindows()

    def detect_panic(self, white_percent: float):
        if 100 < self.frame_count:
            if white_percent > 0.95:
                self.panicDetected()
