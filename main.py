import cv2
import numpy as np
from ppadb.client import Client as AdbClient
import random
import sys
import time

class DroneiaBot:
    def __init__(self):
        self.template_path_green = '../pythonQA/Screenshot_20230707-035200_ .jpg'
        self.template_path_white = '../pythonQA/Screenshot_20230707-042947_ .jpg'
        self.work_path = '../pythonQA/Screenshot_20230707-060419_ .jpg'
        self.benner_path = '../pythonQA/Screenshot_20230707-142628_ .jpg'
        self.preferences_path = '../pythonQA/Screenshot_20230707-165943_ .jpg'
        self.bottom_right_2 = []

        # ADB 클라이언트 초기화
        self.adb = AdbClient(host="127.0.0.1", port=5037)
        self.devices = self.adb.devices()

        if len(self.devices) == 0:
            print("연결된 디바이스가 없습니다.")
            sys.exit()

        # 첫 번째 디바이스 선택
        self.device = self.devices[0]

    def capture_screen(self):
        # 모바일 디바이스의 스크린샷 캡처
        image = self.device.screencap()
        img_data = np.array(image, dtype=np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        return img

    def find_template(self, image, template):
        # 이미지에서 템플릿 매칭
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        return max_val, max_loc

    def benner_ui_coordinates(self):
        # UI 요소의 좌표 계산
        screen_img = self.capture_screen()

        # 템플릿 이미지 로드
        benner_img = cv2.imread(self.benner_path)
        # 템플릿 매칭
        benner_max_val, benner_max_loc = self.find_template(screen_img, benner_img)

        # 좌표 계산
        benner_template_width = benner_img.shape[1]
        benner_template_height = benner_img.shape[0]
        benner_top_left = benner_max_loc
        benner_bottom_right = (benner_top_left[0] + benner_template_width, benner_top_left[1] + benner_template_height)
        print("상단 왼쪽 (x, y):", benner_top_left)
        print("하단 오른쪽 (x, y):", benner_bottom_right)
        return benner_top_left, benner_bottom_right

    def calculate_ui_coordinates(self):
        # UI 요소의 좌표 계산
        screen_img = self.capture_screen()

        # 템플릿 이미지 로드
        template_img = cv2.imread(self.template_path_green)
        # 템플릿 매칭
        max_val, max_loc = self.find_template(screen_img, template_img)

        # 좌표 계산
        template_width = template_img.shape[1]
        template_height = template_img.shape[0]
        top_left = max_loc
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        print("상단 왼쪽 (x, y):", top_left)
        print("하단 오른쪽 (x, y):", bottom_right)
        self.bottom_right_2.append([bottom_right[0] * 2, bottom_right[1]])
        print(self.bottom_right_2)
        if not top_left[0] == 0:
            print('error')
            template_img = cv2.imread(self.template_path_white)
            # 템플릿 매칭
            max_val, max_loc = self.find_template(screen_img, template_img)

            # 좌표 계산
            template_width = template_img.shape[1]
            template_height = template_img.shape[0]
            top_left = max_loc
            bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        return top_left, bottom_right

    def run(self):
        command = f"am start -n com.thedash.droneia/.activity.MainActivity"
        result = self.device.shell(command)
        time.sleep(2)
        print(f"Successfully launched")

        # UI 좌표 계산
        benner_top_left, benner_bottom_right = self.benner_ui_coordinates()
        top_left, bottom_right = self.calculate_ui_coordinates()
        center_x = (top_left[0] + bottom_right[0]) / 2
        center_y = (top_left[1] + bottom_right[1]) / 2

        benner_center_x = (benner_top_left[0] + benner_bottom_right[0]) / 2
        benner_center_y = (benner_top_left[1] + benner_bottom_right[1]) / 2

        x2 = bottom_right[0]
        y2 = top_left[1]

        center_x2 = (x2 + self.bottom_right_2[0][0]) / 2
        center_y2 = (y2 + self.bottom_right_2[0][1]) / 2
        print("UI 좌표:")
        print("상단 왼쪽 (x, y):", top_left)
        print("하단 오른쪽 (x, y):", bottom_right)
        print(center_x, center_y)

        def ran1():
            command = f'input tap {center_x} {center_y}'
            result = self.device.shell(command)
            print(f'발주: touching {center_x, center_y}')

        def ran2():
            command = f'input tap {center_x * 3} {center_y}'
            result = self.device.shell(command)
            print(f'수주: touching {center_x * 3, center_y}')

        def ran3():
            command = f'input tap {center_x * 5} {center_y}'
            result = self.device.shell(command)
            print(f'구인: touching {center_x * 5, center_y}')

        def ran4():
            command = f'input tap {center_x * 7} {center_y}'
            result = self.device.shell(command)
            print(f'마이페이지: touching {center_x * 7, center_y}')

        command = f'input tap {benner_center_x} {benner_center_y}'
        result = self.device.shell(command)

        functions = [ran1, ran2, ran3, ran4]
        while True:
            random_func = random.choice(functions)
            random_func()


# Create an instance of the DroneiaBot class
bot = DroneiaBot()
bot.run()
