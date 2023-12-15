import zed
import cv2
import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 or args[1] not in ['mini', '2i']:
        print("Usage: python zed_exp_gain_record.py mini (or 2i)")
        exit(0)
    cam_model = args[1] # cam_model: 2i or mini
    cam = zed.ZEDCamera(model=cam_model)
    
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        left_2i, right_2i = cam.get_image()
        img_size = left_2i.shape[:2]
        left_2i = cv2.resize(left_2i, (int(img_size[1]), int(img_size[0]*2)), interpolation=cv2.INTER_LINEAR)
        right_2i = cv2.resize(right_2i, (int(img_size[1]), int(img_size[0]*2)), interpolation=cv2.INTER_LINEAR)
        image_concat = cv2.hconcat([left_2i, right_2i])
        cv2.imshow("Image", image_concat)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
    cam.cam_close()