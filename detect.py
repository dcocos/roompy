# USAGE
# python pi_surveillance.py --conf conf.json

import argparse
import datetime
import json
import time
import warnings

import cv2
import imutils
from picamera import PiCamera
# import the necessary packages
from picamera.array import PiRGBArray

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
                help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
client = None

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0


cap = cv2.VideoCapture(Camera#);

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

while (1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame', fgmask)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# # capture frames from the camera
# for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     # grab the raw NumPy array representing the image and initialize
#     # the timestamp and occupied/unoccupied text
#     frame = f.array
#     timestamp = datetime.datetime.now()
#     text = "Available"
#
#     # resize the frame, convert it to grayscale, and blur it
#     frame = imutils.resize(frame, width=800)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (21, 21), 0)
#
#     # if the average frame is None, initialize it
#     if avg is None:
#         print("[INFO] starting background model...")
#         avg = gray.copy().astype("float")
#         rawCapture.truncate(0)
#         continue
#
#     # accumulate the weighted average between the current frame and
#     # previous frames, then compute the difference between the current
#     # frame and running average
#     cv2.accumulateWeighted(gray, avg, 0.5)
#     frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
#
#     # threshold the delta image, dilate the thresholded image to fill
#     # in holes, then find contours on thresholded image
#     thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
#                            cv2.THRESH_BINARY)[1]
#     thresh = cv2.dilate(thresh, None, iterations=2)
#     cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#                             cv2.CHAIN_APPROX_SIMPLE)
#     cnts = imutils.grab_contours(cnts)
#
#     # loop over the contours
#     for c in cnts:
#         # if the contour is too small, ignore it
#         if cv2.contourArea(c) < conf["min_area"]:
#             continue
#
#         # compute the bounding box for the contour, draw it on the frame,
#         # and update the text
#         (x, y, w, h) = cv2.boundingRect(c)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         text = "Unavailable"
#
#     # draw the text and timestamp on the frame
#     ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
#     cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#     cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.35, (0, 0, 255), 1)
#
#     # check to see if the room is unavailable
#     if text == "Unavailable":
#         # check to see if enough time has passed between uploads
#         if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
#             # increment the motion counter
#             motionCounter += 1
#
#             # check to see if the number of frames with consistent motion is
#             # high enough
#             if motionCounter >= conf["min_motion_frames"]:
#                 # update the last uploaded timestamp and reset the motion
#                 # counter
#                 lastUploaded = timestamp
#                 motionCounter = 0
#
#     # otherwise, the room is not occupied
#     else:
#         motionCounter = 0
#
#     # check to see if the frames should be displayed to screen
#     if conf["show_video"]:
#         # display the roompy window
#         cv2.imshow("Roompy", frame)
#         key = cv2.waitKey(1) & 0xFF
#
#         # if the `q` key is pressed, break from the lop
#         if key == ord("q"):
#             break
#
#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)
