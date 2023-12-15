import zed
import cv2
import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 or args[1] not in ['mini', '2i']:
        print("Usage: python zed_exp_gain_record.py mini (or 2i)")
        exit(0)
    cam_model = args[1] # cam_model: 2i or mini
    cam = zed.ZEDCamera(model=cam_model, resolution='1080')

    monitor_x = 2560    # 주모니터의 x축 길이
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Image",monitor_x,0)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 아래 주석을 해제하여 exposure, gain 값을 조정할 수 있습니다.
    # cam.set_camera_setting(cam.EXPOSURE, 0)
    # cam.set_camera_setting(cam.GAIN, 50)
    
    while True:
        left_2i, right_2i = cam.get_image()
        image_concat = cv2.hconcat([left_2i, right_2i])
        cv2.imshow("Image", image_concat)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    cam.cam_close()
