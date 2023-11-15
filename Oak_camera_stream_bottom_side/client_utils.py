import os
import shutil
import winsound
import subprocess
from threading import Thread

import cv2


def create_dir(path):
    """Creates folder if it doesn't exit

    Args:
        path: path to folder.
    """
    if not os.path.isdir(path):
        os.mkdir(path)


def streams_path(stream_folder_path, stream_name):
    """Returns the path to new stream file

    Args:
        stream_folder_path: path to stream folder.
        stream_name: type of stream.

    Returns:
        new_stream_path: path to stream
    """
    # streams path
    streams_list = os.listdir(os.path.join(stream_folder_path))
    if len(streams_list):
        # sort based on the stream number
        streams_list.sort(key=lambda x: int(x.split("_")[0]))
        # add 1 to stream name
        new_stream_path = os.path.join(
            stream_folder_path,
            "{}_{}".format(
                int(streams_list[-1].split("_")[0]) + 1, stream_name
            ),
        )
        return new_stream_path
    # first stream name
    new_stream_path = os.path.join(
        stream_folder_path,
        "{}_{}".format(1, stream_name),
    )
    return new_stream_path


def data_folder_handler(directory=None):
    """Returns the path to new stream files and creates missing folders

    Args:
        directory (optional): path to main data folder

    Returns:
        MISSION_STREAM_PATH: path to mission stream
        MODEL_STREAM_PATH: path to model stream
        DEPTH_VIEW_PATH: path to stereo stream
        AGISOFT_MODELS_PATH: path to AGISOFT models
    """
    # current client directory
    CLIENT_DIR = (
        directory if directory is not None else os.path.dirname(__file__)
    )
    # create data directory if it doesn't exit
    DATA_DIR = os.path.join(CLIENT_DIR, "data")
    create_dir(DATA_DIR)
    # create folders for mission, stereo and modeling streams
    MISSION_DIR = os.path.join(DATA_DIR, "mission_stream")
    DEPTH_DIR = os.path.join(DATA_DIR, "depth_view")
    MODEL_DIR = os.path.join(DATA_DIR, "model_stream")
    AGISOFT_DIR = os.path.join(DATA_DIR, "agisoft_models")
    create_dir(MISSION_DIR)
    create_dir(DEPTH_DIR)
    create_dir(MODEL_DIR)
    create_dir(AGISOFT_DIR)
    # path of streams
    MISSION_STREAM_PATH = streams_path(MISSION_DIR, stream_name="stream.mp4")
    MODEL_STREAM_PATH = streams_path(MODEL_DIR, stream_name="model.mp4")
    DEPTH_VIEW_PATH = streams_path(DEPTH_DIR, stream_name="stereo")
    AGISOFT_MODELS_PATH = streams_path(AGISOFT_DIR, stream_name="model")
    return (
        MISSION_STREAM_PATH,
        MODEL_STREAM_PATH,
        DEPTH_VIEW_PATH,
        AGISOFT_MODELS_PATH,
    )


def create_stream_recorder(
    stream_path, FOURCC=["m", "p", "4", "v"], DIMENSION=(640, 400), FPS=20
):
    """returns video recorder

    Args:
        stream_path: videowriter created to record mission or model streams

    Returns:
        video_writer: writer created to record mission or model streams
    """
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*FOURCC)
    video_writer = cv2.VideoWriter(stream_path, fourcc, FPS, DIMENSION)
    return video_writer


def create_stereo_directory(path):
    """Creates stereo directory in depth_view folder

    Args:
        path: path to depth_view folder
    """
    os.mkdir(path=path)


def create_agisoft_directory(path):
    """Creates agisoft model directory in agisoft_models folder

    Args:
        path: path to agisoft_models folder
    """
    os.mkdir(path=path)
    os.mkdir(path=os.path.join(path, "input"))
    os.mkdir(path=os.path.join(path, "output"))


def render_stream(stream_recorder, frames_q):
    """Renders given frame into stream
    Args:
        stream_recorder: writer created to record mission or model streams
        frames_q: a queue that has the current frame to be rendered
    """
    stream_recorder.write(frames_q.get())


def streams_threads(stream_q, stream_recorder, stream_thread_list, frame):
    """Handles mission and model streams

    Args:
        frames_q: a queue that will put the current frame to be rendered
        stream_recorder: writer created to record mission or model streams
        stream_thread_list: a list that will append the started thread
        frame: frame to be rendered
    """
    if stream_q.empty():
        if len(stream_thread_list):
            stream_thread_list[0].join()
            stream_thread_list.pop()
        stream_q.put(frame)
        rgb_thread = Thread(
            target=render_stream, args=(stream_recorder, stream_q)
        )
        rgb_thread.start()
        stream_thread_list.append(rgb_thread)


def stereo_writer(stereo_stream_q, stereo_stream, stereo_count):
    """Wries stereo frame to stereo directory

    Args:
    stereo_stream_q: a queue that will put the current stereo frame to be saved in stereo directory
    stereo_stream: path to stereo directory
    stereo_count: current frame count (should be incremented before calling the function to avoid overwirting existing frames)
    """
    cv2.imwrite(
        filename=os.path.join(stereo_stream, "{}.png".format(stereo_count)),
        img=stereo_stream_q.get(),
    )


def stereo_thread(
    stereo_stream_q, stereo_stream, stereo_threads_list, frame, stereo_count
):
    """Handles stereo frames

    Args:
    stereo_stream_q: a queue that will put the current stereo frame to be saved in stereo directory
    stereo_stream: path to stereo directory
    stereo_threads_list: a list that will append the started thread
    frame: stereo frame to be rendered
    stereo_count: current frame count (should be incremented before calling the function to avoid overwirting existing frames)
    """
    if stereo_stream_q.empty():
        if len(stereo_threads_list):
            stereo_threads_list[0].join()
            stereo_threads_list.pop()
        stereo_stream_q.put(frame)
        stereo_thread = Thread(
            target=stereo_writer,
            args=(stereo_stream_q, stereo_stream, stereo_count),
        )
        stereo_thread.start()
        stereo_threads_list.append(stereo_thread)


def release_writers(stream_recorder, stream_thread_list):
    """Releases writers and join threads

    Args:
        stream_recorder: writer created to record mission or model streams
        stream_thread_list: a list that has the started threads
    """
    if len(stream_thread_list):
        stream_thread_list[0].join()
        stream_thread_list.pop()
    stream_recorder.release()


def AgiSoftThread(agisoft_stream, model_stream):
    """Thread that opens agisoft in a separate process

    Args:
        agisoft_stream: depth images used to extract 3d model
    """
    if len(os.listdir("E:\depth_view")):
        shutil.rmtree("E:\depth_view\{}".format(os.listdir("E:\depth_view")[0]))
    if len(os.listdir("E:\model_stream")):
        os.remove("E:\model_stream\{}".format(os.listdir("E:\model_stream")[0]))
    winsound.Beep(2500, 200)
    shutil.copytree(agisoft_stream, "E:\depth_view\{}".format(agisoft_stream.split("\\")[-1]))
    shutil.copy(model_stream, "E:\model_stream\{}".format(model_stream.split("\\")[-1]))
    winsound.Beep(2500, 200)
    winsound.Beep(2500, 200)
    winsound.Beep(2500, 200)
