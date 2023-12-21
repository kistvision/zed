import zed
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import time
from collections import deque
import json

save_dir = '/home/vision/test/'
    
if __name__ == "__main__":
    with open('{0}/video_info.json'.format(save_dir), 'r') as info:
        json_data = json.load(info)
        FPS = float(json_data['FPS'])
        VIDEO_LENGTH = int(json_data['number_of_frames'])
    # 3D projector
    vw_3DP = cv2.VideoWriter('{0}/video_for_3D_projector.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (1920, 1080))
    # Nreal Glasses
    vw_ARG = cv2.VideoWriter('{0}/video_for_AR_glasses.mp4'.format(save_dir), cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), FPS, (3840, 1080))
    for i in tqdm(range(VIDEO_LENGTH)):
        left = cv2.imread('{0}/left/{1}.png'.format(save_dir, i))
        right = cv2.imread('{0}/right/{1}.png'.format(save_dir, i))
        left_1080 = cv2.resize(left, (1920, 1080), interpolation=cv2.INTER_LINEAR)
        right_1080 = cv2.resize(right, (1920, 1080), interpolation=cv2.INTER_LINEAR)
        image_concat = cv2.hconcat([left_1080, right_1080])
        vw_ARG.write(image_concat)
        img_size = left.shape[:2]
        left = cv2.resize(left, (960, 1080), interpolation=cv2.INTER_LINEAR)
        right = cv2.resize(right, (960, 1080), interpolation=cv2.INTER_LINEAR)
        image_concat = cv2.hconcat([left, right])
        vw_3DP.write(image_concat)
    vw_3DP.release()
    vw_ARG.release()

