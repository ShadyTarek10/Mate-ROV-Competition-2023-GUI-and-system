import subprocess
from threading import *
from multiprocessing.connection import Listener
import sys
import cv2 as cv
import numpy as np
import torch
from sendjoysticksocket import clientgui


hamo = [
    x,
    o,
    sqr,
    tri,
    share,
    ps,
    options,
    left_scroll_button,
    right_scroll_button,
    l1,
    r1,
    upward,
    downward,
    left,
    right,
    touch_pad,
    xaxl,
    yaxl,
    l2,
    r2,
    xaxr,
    yaxr,
]
hamo[2] = 1
adrr = ("localhost", 7600)
lis = Listener(adrr, authkey=b"bsc")
print(adrr)
conn2 = lis.accept()
count = 0
ratio_with_error_x = 0
ratio_with_error_y = 0
margin_error = 500
margin_error_new = 0
model = torch.hub.load(
    "C:/Users/Shady/Desktop/yolov5",
    "custom",
    path="D:/Kolya/Term 7/Microprocessor lab/12 lab/best (1).pt",
    source="local",
)


def move_right_left(x):
    if x == 1700:
        hamo[20] = 0.9
    else:
        hamo[20] = -0.9


def move_up_down(x):
    if x == 1700:
        hamo[21] = 1
    else:
        hamo[21] = -1


def move_forward(x, z):
    if z <= 300:
        print("press button")
        return
    hamo[17] = 1


def Camhandler1():
    while True:
        frame = conn2.recv()
        x_center = int(frame.shape[1] / 2)
        y_center = int(frame.shape[0] / 2)
        ############## YOLO ###############
        tmp = model(frame).pandas().xyxy[0]
        ########################## depth #########################
        # cv.rectangle(rgb,(x_center-margin_error,y_center-margin_error),(x_center+margin_error,y_center+margin_error),(255,0,0),3)
        z = 0
        length = 0
        Width = 0
        for i in range(len(tmp)):
            if tmp["confidence"][i] > 0.5:
                length = tmp["xmax"][i] - tmp["xmin"][i]
                Width = tmp["ymax"][i] - tmp["ymin"][i]
        x_button, y_button = 0, 0
        if count == 0:
            prev_length = length
            prev_width = Width
        else:
            # change roi
            ratio_with_error_x = length - prev_length
            ratio_with_error_y = Width - prev_width
        if ratio_with_error_x <= ratio_with_error_y:
            margin_error_new = margin_error - ratio_with_error_x
        else:
            margin_error_new = margin_error - ratio_with_error_y
        margin_error_new = max(margin_error_new, 100)
        cv.rectangle(
            frame,
            (
                int(abs(x_center - margin_error_new)),
                int(abs(y_center - margin_error_new)),
            ),
            (
                int(abs(x_center + margin_error_new)),
                int(abs(y_center + margin_error_new)),
            ),
            (255, 0, 0),
            3,
        )
        for i in range(len(tmp)):
            #    if tmp[‘confidence’][i]>0.5:
            x_button = int((tmp["xmin"][i] + tmp["xmax"][i]) / 2)
            y_button = int((tmp["ymin"][i] + tmp["ymax"][i]) / 2)
            cv.rectangle(
                frame,
                (int(tmp["xmin"][i]), int(tmp["ymin"][i])),
                (int(tmp["xmax"][i]), int(tmp["ymax"][i])),
                (0, 255, 0),
                3,
            )
        cv.imshow("rgb", frame)
        ##################### RATIO #########################
        x_diff = x_button - x_center
        y_diff = y_button - y_center
        # print(x_diff)
        if (
            (abs(x_button) < x_center + margin_error_new)
            and (abs(x_button) > x_center - margin_error_new)
            and (abs(y_button) > y_center - margin_error_new)
            and (abs(y_button) < y_center + margin_error_new)
        ):
            move_forward(1700, z)
        else:
            if x_diff < 0:
                move_right_left(1700)
            else:
                move_right_left(1500)
            if y_diff < 0:
                move_up_down(1700)
            else:
                move_up_down(1500)
        count += 1
        key = cv.waitKey(1)
        if key == ord("q"):
            break

