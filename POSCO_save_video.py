import zed
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import time
from collections import deque
import json
import psutil

def memory_usage(message: str = 'debug'):
    # current process RAM usage
    p = psutil.Process()
    rss = p.memory_info().rss / 2 ** 20 # Bytes to MB
    print(f"[{message}] memory usage: {rss: 10.5f} MB")

save_dir = '/home/vision/zed_stereo_video/mini'
if not os.path.exists('{0}'.format(save_dir)):
    os.mkdir(save_dir)
    
if __name__ == "__main__":
    FPS = 10
    video_length = 60.      # seconds
    # 3D projector
    # vw_left = cv2.VideoWriter('{0}/video_left.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1920, 1080))
    # vw_right = cv2.VideoWriter('{0}/video_right.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1920, 1080))
    vw_left = cv2.VideoWriter('{0}/video_left.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1280, 720))
    vw_right = cv2.VideoWriter('{0}/video_right.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1280, 720))
    # vw_left = cv2.VideoWriter('{0}/video_left.avi'.format(save_dir), cv2.VideoWriter_fourcc( 'X', 'V', 'I', 'D'), FPS, (1920, 1080))
    # vw_right = cv2.VideoWriter('{0}/video_right.avi'.format(save_dir), cv2.VideoWriter_fourcc('i','y','u','v'), FPS, (1920, 1080))
    # vw_left = cv2.VideoWriter('{0}/video_left.avi'.format(save_dir), cv2.VideoWriter_fourcc( 'X', 'V', 'I', 'D'), FPS, (1280, 720))
    # vw_right = cv2.VideoWriter('{0}/video_right.avi'.format(save_dir), cv2.VideoWriter_fourcc('i','y','u','v'), FPS, (1280, 720))
    # vw_left = cv2.VideoWriter('{0}/video_left.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1280, 720))
    # vw_right = cv2.VideoWriter('{0}/video_right.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1280, 720))
    cam = zed.ZEDCamera(model='mini', resolution='720')
    cam.set_camera_setting(cam.EXPOSURE, 0)
    cam.set_camera_setting(cam.GAIN, 50)
    time.sleep(1.0)

    start = time.time()
    sequences = 0
    while True:
        left, right = cam.get_image()
        # b,g,r,a = cv2.split(left)
        # left = cv2.merge((b, g, r))
        # b,g,r,a = cv2.split(right)
        # right = cv2.merge((b, g, r))
        # left = left[:,:,:3]
        # right = right[:,:,:3]
        left = cv2.cvtColor(left, cv2.COLOR_BGRA2BGR)
        right = cv2.cvtColor(right, cv2.COLOR_BGRA2BGR)
        vw_left.write(left)
        vw_right.write(right)
        t = time.time() - start
        sequences += 1
        print(t)
        if t > video_length:
            break
    vw_left.release()
    vw_right.release()
    cam.cam_close()
    memory_usage('')
    FPS = sequences / video_length
    print("FPS: ", FPS)
    # exit(0)

    # Make json file
    json_data = {}
    json_data['number_of_frames'] = sequences
    json_data['length_of_video'] = video_length
    json_data['FPS'] = FPS
    with open('{0}/video_info.json'.format(save_dir), 'w') as info:
        json.dump(json_data, info, indent=4)


    cap_left = cv2.VideoCapture('{0}/video_left.mp4'.format(save_dir))
    cap_right = cv2.VideoCapture('{0}/video_right.mp4'.format(save_dir))
    index = 0

    if 'left' not in os.listdir('{0}'.format(save_dir)):
        os.mkdir('{0}/left'.format(save_dir))
    if 'right' not in os.listdir('{0}'.format(save_dir)):
        os.mkdir('{0}/right'.format(save_dir))
    print("left")
    while cap_left.isOpened():
        ret, frame = cap_left.read()
        if ret is False:
            break
        cv2.imwrite('{0}/left/{1}.png'.format(save_dir, index), frame)
        index += 1
    cap_left.release()

    print("right")
    index = 0
    while cap_right.isOpened():
        ret, frame = cap_right.read()
        if ret is False:
            break
        cv2.imwrite('{0}/right/{1}.png'.format(save_dir, index), frame)
        index += 1
    cap_right.release()