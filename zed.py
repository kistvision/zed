import sys
import pyzed.sl as sl
import numpy as np

class ZEDCamera():
    def __init__(self, model='2i', resolution='1080'):
        print("Initializing...")
        self.model = model
        init = sl.InitParameters()
        for i in range(2):
            init.set_from_camera_id(i)
            if resolution == '1080':
                init.camera_resolution = sl.RESOLUTION.HD1080
            elif resolution == '720':
                init.camera_resolution = sl.RESOLUTION.HD720
            else:
                print("Put a correct resolution")
                exit(0)

            self.cam = sl.Camera()
            if not self.cam.is_opened():
                print("Opening ZED Camera...")
            status = self.cam.open(init)
            if status != sl.ERROR_CODE.SUCCESS:
                print(repr(status))
                exit()

            self.camera_information = self.cam.get_camera_information()
            self.cam_model = str(self.camera_information.camera_model).rstrip()
            print(model, self.cam_model)
            if model == '2i' and self.cam_model == 'ZED 2i':
                print("Start ZED 2i")
                break
            elif model == 'mini' and self.cam_model == 'ZED-M':
                print("Start ZED mini")
                break

            self.cam_close()
            print("Camera bringup was failed")
            exit(0)

        self.runtime = sl.RuntimeParameters()
        
        # for ZED SDK < 4.0
        # image_size = self.cam.get_camera_information().camera_resolution

        # for ZED SDK > 4.0
        image_size = self.camera_information.camera_configuration.resolution

        self.W, self.H = image_size.width, image_size.height
        self.roi = sl.Rect()
        self.select_in_progress = False
        self.origin_rect = (-1,-1 )

        self.mat_left = sl.Mat(self.W, self.H)
        self.mat_right = sl.Mat(self.W, self.H)

        self.BRIGHTNESS = sl.VIDEO_SETTINGS.BRIGHTNESS
        self.CONTRAST = sl.VIDEO_SETTINGS.CONTRAST
        self.EXPOSURE = sl.VIDEO_SETTINGS.EXPOSURE
        self.GAIN = sl.VIDEO_SETTINGS.GAIN
        self.GAMMA = sl.VIDEO_SETTINGS.GAMMA
        self.HUE = sl.VIDEO_SETTINGS.HUE
        self.SATURATION = sl.VIDEO_SETTINGS.SATURATION
        self.SHARPNESS = sl.VIDEO_SETTINGS.SHARPNESS
        self.WHITEBALANCE_TEMPERATURE = sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE
        self.SETTINGS = [self.BRIGHTNESS, self.CONTRAST, self.EXPOSURE, self.GAIN, self.GAMMA,
                         self.HUE, self.SATURATION, self.SHARPNESS, self.WHITEBALANCE_TEMPERATURE]

        
        self.init_camera_parameter()
    def init_camera_parameter(self):
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.BRIGHTNESS, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.CONTRAST, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.GAIN, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.GAMMA, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.HUE, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SATURATION, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.SHARPNESS, -1)
        self.cam.set_camera_settings(sl.VIDEO_SETTINGS.WHITEBALANCE_TEMPERATURE, -1)
        print("Camera parameters are initialized!")

    def set_camera_setting(self, setting, value):
        self.cam.set_camera_settings(setting, value)

    def get_image(self):
        err = self.cam.grab(self.runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            self.cam.retrieve_image(self.mat_left, sl.VIEW.LEFT)
            left_image = self.mat_left.get_data()
            self.cam.retrieve_image(self.mat_right, sl.VIEW.RIGHT)
            right_image = self.mat_right.get_data()
            return left_image, right_image
        else:
            image = np.zeros((self.W, self.H))
            return image, image
    
    def cam_close(self):
        self.cam.close()
        print("\nFINISH")

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2 or args[1] not in ['mini', '2i']:
        print("Usage: python zed_exp_gain_record.py mini (or 2i)")
        exit(0)
    cam_model = args[1] # cam_model: 2i or mini
    cam = ZEDCamera(model=cam_model)
    import cv2
    while True:
        left, right = cam.get_image()
        cv2.imshow("image", right)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cam.cam_close()