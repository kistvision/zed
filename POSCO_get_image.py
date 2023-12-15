import zed
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import time

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 or args[1] not in ['mini', '2i']:
        print("Usage: python POSCO_get_image.py mini (or 2i)")
        exit(0)
    cam_model = args[1] # cam_model: 2i or mini
    cam = zed.ZEDCamera(model=cam_model)
    cam.set_camera_setting(cam.EXPOSURE, 0)
    cam.set_camera_setting(cam.GAIN, 0)
    # cv2.waitKey(1000)
    time.sleep(5)
    # for i in tqdm(range(80,100)):
    #     for j in range(80,100):
    for i in tqdm(range(10)):
        for j in range(10):
            # time.sleep(0.1)
            left, right = cam.get_image()
            cam.set_camera_setting(cam.EXPOSURE, int(i*10))
            cam.set_camera_setting(cam.GAIN, int(j*10))

            time.sleep(0.2)

            exposure = cam.cam.get_camera_settings(cam.EXPOSURE)
            gain = cam.cam.get_camera_settings(cam.GAIN)
            # if i != exposure[-1] or j != gain[-1]:
            #     print("error / exposure, i, gain, j", exposure, i, gain, j)

            cv2.imwrite('./images_zed{0}/img_left_exp{1}_gain{2}.png'.format(cam_model, i*10, j*10), left)
            cv2.imwrite('./images_zed{0}/img_right_exp{1}_gain{2}.png'.format(cam_model, i*10, j*10), right)
            # if j == 0:
            #     cv2.imwrite('./images_zed{0}/img_left_exp{1}_gain{2}.png'.format(cam_model, (i-1)*10, 90), left)
            #     cv2.imwrite('./images_zed{0}/img_right_exp{1}_gain{2}.png'.format(cam_model, (i-1)*10, 90), right)
            # else:
            #     cv2.imwrite('./images_zed{0}/img_left_exp{1}_gain{2}.png'.format(cam_model, (i-1)*10, j-10), left)
            #     cv2.imwrite('./images_zed{0}/img_right_exp{1}_gain{2}.png'.format(cam_model, (i-1)*10, j-10), right)

    cam.cam_close()