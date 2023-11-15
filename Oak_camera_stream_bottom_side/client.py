import ctypes
import time
from queue import Queue
from threading import Thread

import cv2
import numpy as np

from client_utils import *
from station_netgear_client import NetgearClient

# full screen resolution
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def main():
    # get streams paths
    (
        mission_stream,
        model_stream,
        stereo_stream,
        agisoft_model_dir,
    ) = data_folder_handler()
    agisoft_stream = model_stream
    # get mission and model streams recorder
    mission_recorder, model_recorder = create_stream_recorder(
        mission_stream, FPS=30
    ), create_stream_recorder(model_stream, FPS=30)
    # create stereo folder
    create_stereo_directory(stereo_stream)
    # create agisoft_models folder
    create_agisoft_directory(agisoft_model_dir)
    # counter for stereo images
    stereo_counter = 0
    # create a list for streams threads
    mission_threads_list, model_threads_list, stereo_threads_list = [], [], []
    # queue that saves an instance for each stream data
    mission_stream_q, model_stream_q, stereo_stream_q = (
        Queue(maxsize=1),
        Queue(maxsize=1),
        Queue(maxsize=1),
    )
    netgear = NetgearClient(ADDRESS="192.168.33.100")
    # tic is mainly used to save stereo frame every 0.5 second
    tic = time.time()
    # agi_tic used to call agisoft once every 10 seconds
    agi_tic = time.time()
    # agi soft flag that allows agisoft to start after stereo termination
    AGISOFT = False
    # state of client
    CLIENT = "rgb"
    # state of server
    SERVER = "rgb"
    # record model flag
    RECORD = False
    while True:
        SERVER, data = netgear.client.recv(return_data=CLIENT)
        # handling data that we received from server.
        if SERVER == "rgb":
            rgb = data
            streams_threads(
                mission_stream_q, mission_recorder, mission_threads_list, rgb
            )
            cv2.imshow("OAK CAMERA STREAM", cv2.resize(rgb, (width, height)))
        if SERVER == "rgb_depth":
            rgb = np.uint8(data[:, :640])
            right, disparity, depth = cv2.split(data[:, 640:])
            right = np.uint8(right)
            right = cv2.cvtColor(right, cv2.COLOR_BGRA2BGR)
            disparity = np.uint8(disparity)
            disparity = cv2.cvtColor(disparity, cv2.COLOR_BGRA2BGR)
            stacked = np.vstack(
                [
                    cv2.resize(
                        np.hstack([rgb, np.zeros_like(rgb)]), (640, 200)
                    ),
                    cv2.resize(np.hstack([right, disparity]), (640, 200)),
                ]
            )
            streams_threads(
                mission_stream_q,
                mission_recorder,
                mission_threads_list,
                stacked,
            )
            streams_threads(
                model_stream_q, model_recorder, model_threads_list, rgb
            )
            # save stereo frame every 0.5 seconds
            if time.time() - tic > 0.5:
                stereo_thread(
                    stereo_stream_q,
                    stereo_stream,
                    stereo_threads_list,
                    data[:, 640:],
                    stereo_counter,
                )
                stereo_counter += 1
                tic = time.time()
            cv2.imshow(
                "OAK CAMERA STREAM", cv2.resize(stacked, (width, height))
            )
        # client events
        key = cv2.waitKey(1)
        if key == ord("r") or key == ord("R"):
            CLIENT = "rgb"
        if key == ord("f") or key == ord("F"):
            CLIENT = "rgb_depth"
        if key == ord("t") or key == ord("T"):
            if SERVER == "rgb_depth":
                release_writers(model_recorder, model_threads_list)
                CLIENT = "rgb"
                AGISOFT = True
        if key == ord("a") or key == ord("A"):
            if time.time() - agi_tic > 10 and AGISOFT:
                agi_tic = time.time()
                agisoft = Thread(
                    target=AgiSoftThread,
                    args=(stereo_stream, model_stream,),
                )
                agisoft.start()
        if key == ord("n") or key == ord("n"):
            AGISOFT = False
            (
                _,
                model_stream,
                stereo_stream,
                agisoft_model_dir,
            ) = data_folder_handler()
            model_recorder = create_stream_recorder(model_stream, FPS=30)
            create_stereo_directory(stereo_stream)
            create_agisoft_directory(agisoft_model_dir)
            stereo_counter = 0
            agisoft_stream = model_stream
        if key == ord("q"):
            break
    release_writers(mission_recorder, mission_threads_list)
    release_writers(model_recorder, model_threads_list)
    # close client
    netgear.client.close()


if __name__ == "__main__":
    main()
