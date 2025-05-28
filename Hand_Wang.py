import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import autopy
import pyautogui
import mediapipe as mp
import cv2
from My_gui import Ui_MainWindow

class HandThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    change_text_signal = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.prev_gesture = None  # 用于存储上一帧的手势

    def run(self):
        draw = True
        frameR = 150
        smoothening = 8
        step = 1
        w_camera, h_camera = 1280, 720

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w_camera)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h_camera)
        loc_x, loc_y = 0, 0
        # w_screen, h_screen = autopy.screen.size()
        w_screen, h_screen = pyautogui.size()

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                              max_num_hands=2,
                              min_detection_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils

        while True:
            success, img = self.cap.read()

            if Flip_sign == True:
                img = cv2.flip(img, 1)

            if not success:
                continue
            image_height, image_width, _ = np.shape(img)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            length = np.size(results.multi_hand_landmarks)
            textImage = np.zeros((500, 300, 3), np.uint8)

            if Hand_gesture:
                if results.multi_hand_landmarks:
                    if length == 1:
                        hand = results.multi_hand_landmarks[0]
                        label_a = results.multi_handedness[0]
                        if draw:
                            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

                        list_a = self.collect_keypoints(hand, image_width, image_height)
                        list_a_1, hull_a = self.draw_hull(list_a)
                        list_fingertips = [4, 8, 12, 16, 20]
                        up_fingers_a = self.find_up_fingers(list_a_1, hull_a, list_fingertips)
                        str_guester_a = self.get_str_guester(up_fingers_a, list_a_1)
                        # 显示识别结果
                        x0 = list_a[0][0]
                        y0 = list_a[0][1]
                        cv2.putText(img, ' %s' % (str_guester_a), (x0, y0), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 0),
                                    3,
                                    cv2.LINE_AA)
                        cv2.putText(textImage, "This is " + label_a.classification[0].label + " hand, ",
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, "the gesture is " + str_guester_a + '.',
                                    (25, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)

                    if length == 2:
                        hand1 = results.multi_hand_landmarks[1]
                        hand2 = results.multi_hand_landmarks[0]
                        label_a = results.multi_handedness[1]
                        label_b = results.multi_handedness[0]

                        if draw:
                            mpDraw.draw_landmarks(img, hand1, mpHands.HAND_CONNECTIONS)
                            mpDraw.draw_landmarks(img, hand2, mpHands.HAND_CONNECTIONS)

                        list_a = self.collect_keypoints(hand1, image_width, image_height)
                        list_b = self.collect_keypoints(hand2, image_width, image_height)
                        list_a_1, hull_a = self.draw_hull(list_a)
                        list_b_1, hull_b = self.draw_hull(list_b)

                        list_fingertips = [4, 8, 12, 16, 20]
                        up_fingers_a = self.find_up_fingers(list_a_1, hull_a, list_fingertips)
                        up_fingers_b = self.find_up_fingers(list_b_1, hull_b, list_fingertips)
                        # 识别手势
                        str_guester_a = self.get_str_guester(up_fingers_a, list_a_1)
                        str_guester_b = self.get_str_guester(up_fingers_b, list_b_1)

                        x0 = list_a[0][0]
                        y0 = list_a[0][1]
                        x1 = list_b[0][0]
                        y1 = list_b[0][1]

                        # 显示识别结果
                        cv2.putText(img, ' %s' % (str_guester_a), (x0, y0), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 0),
                                    3)
                        cv2.putText(img, ' %s' % (str_guester_b), (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 0),
                                    3)
                        cv2.putText(textImage, "The first hand is ",
                                    (25, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, label_a.classification[0].label + " hand, ",
                                    (25, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, "the gesture is " + str_guester_a + '.',
                                    (25, 130),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, "The second hand is ",
                                    (25, 210),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, label_b.classification[0].label + " hand, ",
                                    (25, 250),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)
                        cv2.putText(textImage, "the gesture is " + str_guester_b + '.',
                                    (25, 290),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8,
                                    (255, 255, 255),
                                    2)

                show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch =show.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(show.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(1280, 720, Qt.IgnoreAspectRatio)
                self.change_pixmap_signal.emit(p)

                show_1 = cv2.cvtColor(textImage, cv2.COLOR_BGR2RGB)  # 图像格式转为RGB
                h_1, w_1, ch_1 = show_1.shape
                bytes_per_line_1 = ch_1 * w_1
                convert_to_qt_format_1 = QImage(show_1.data, w_1, h_1, bytes_per_line_1, QImage.Format_RGB888)
                p_1 = convert_to_qt_format_1.scaled(267, 420, Qt.IgnoreAspectRatio)
                self.change_text_signal.emit(p_1)

            if Mouse_control:
                if results.multi_hand_landmarks:
                    hand = results.multi_hand_landmarks[0]
                    
                    if draw:
                        mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

                    list_a = self.collect_keypoints(hand, image_width, image_height)
                    list_a_1, hull_a = self.draw_hull(list_a)
                    list_fingertips = [4, 8, 12, 16, 20]
                    up_fingers_a = self.find_up_fingers(list_a_1, hull_a, list_fingertips)
                    str_guester_a = self.get_str_guester(up_fingers_a, list_a_1)

                    if str_guester_a == '1':
                        # 进入鼠标移动模式
                        x1 = list_a[8][0]
                        y1 = list_a[8][1]
                        x3 = np.interp(x1, (frameR, w_camera - frameR), (0, w_screen))
                        y3 = np.interp(y1, (100, h_camera - 250), (0, h_screen))
                        # smoothening values
                        loc_x1 = loc_x + (x3 - loc_x) / smoothening * step
                        loc_y1 = loc_y + (y3 - loc_y) / smoothening * step

                        autopy.mouse.move(w_screen - (w_screen - loc_x1), loc_y1)
                        # pyautogui.moveTo(w_screen - (w_screen - loc_x1), loc_y1)

                        cv2.circle(img, (x1, y1), 11, (204, 204, 0), cv2.FILLED)
                        loc_x, loc_y = loc_x1, loc_y1

                        cv2.putText(textImage, 'Mouse Pointer',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)
                    # 当前帧手势为2且上一帧手势不为2时触发鼠标左键点击操作
                    if str_guester_a == '2' and self.prev_gesture != '2':
                        autopy.mouse.click(autopy.mouse.Button.LEFT)
                        # pyautogui.click(button='left')

                        x0 = list_a[12][0]
                        y0 = list_a[12][1]
                        cv2.circle(img, (x0, y0),
                                   11, (128, 255, 0), cv2.FILLED)
                        cv2.putText(textImage, 'Mouse Left',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)

                    if str_guester_a == '3' and self.prev_gesture != '3':
                        x2 = list_a[16][0]
                        y2 = list_a[16][1]
                        cv2.circle(img, (x2, y2),
                                   11, (128, 255, 255), cv2.FILLED)
                        autopy.mouse.click(autopy.mouse.Button.RIGHT)
                        # pyautogui.click(button='right')

                        cv2.putText(textImage, 'Mouse Right',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)

                    if str_guester_a == '4' and self.prev_gesture != '4':
                        x2 = list_a[20][0]
                        y2 = list_a[20][1]
                        cv2.circle(img, (x2, y2),
                                   11, (255, 255, 255), cv2.FILLED)
                        pyautogui.doubleClick()
                        cv2.putText(textImage, 'Double Click',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)
                    # 更新上一帧手势
                    self.prev_gesture = str_guester_a

                    if str_guester_a == '0':
                        x2 = list_a[0][0]
                        y2 = list_a[0][1]
                        cv2.circle(img, (x2, y2),
                                   13, (255, 255, 255), cv2.FILLED)
                        pyautogui.scroll(-100)
                        cv2.putText(textImage, 'Scroll Down',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)

                    if str_guester_a == '5':
                        x2 = list_a[12][0]
                        y2 = list_a[12][1]
                        cv2.circle(img, (x2, y2),
                                   13, (255, 255, 255), cv2.FILLED)
                        pyautogui.scroll(100)
                        cv2.putText(textImage, 'Scroll Up',
                                    (30, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9,
                                    (255, 255, 255),
                                    2)

                show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch =show.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(show.data, w, h, bytes_per_line, QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(1280, 720, Qt.IgnoreAspectRatio)
                self.change_pixmap_signal.emit(p)

                show_1 = cv2.cvtColor(textImage, cv2.COLOR_BGR2RGB)  # 图像格式转为RGB
                h_1, w_1, ch_1 = show_1.shape
                bytes_per_line_1 = ch_1 * w_1
                convert_to_qt_format_1 = QImage(show_1.data, w_1, h_1, bytes_per_line_1, QImage.Format_RGB888)
                p_1 = convert_to_qt_format_1.scaled(267, 420, Qt.IgnoreAspectRatio)
                self.change_text_signal.emit(p_1)
        self.cap.release()

    def collect_keypoints(self, hand, image_width, image_height):
        list_lms = []
        for i in range(21):
            pos_x = hand.landmark[i].x * image_width
            pos_y = hand.landmark[i].y * image_height
            list_lms.append([int(pos_x), int(pos_y)])
        return list_lms
    def draw_hull(self, list_lms):
        list_lms = np.array(list_lms, dtype=np.int32)
        hull_index = [0, 1, 2, 3, 6, 11, 15, 19, 18, 17]
        hull = cv2.convexHull(list_lms[hull_index, :])

        return list_lms, hull
    def find_up_fingers(self, list_lms, hull, ll):

        up_fingers = []

        for i in ll:
            pt = (int(list_lms[i][0]), int(list_lms[i][1]))
            dist = cv2.pointPolygonTest(hull, pt, False)
            if dist < 0:
                up_fingers.append(i)
        return up_fingers
    def get_str_guester(self, up_fingers, list_lms):
        if len(up_fingers) == 1 and up_fingers[0] == 8:
            v1 = list_lms[6] - list_lms[7]
            v2 = list_lms[8] - list_lms[7]
            angle = np.dot(v1, v2) / (np.sqrt(np.sum(v1 * v1)) * np.sqrt(np.sum(v2 * v2)))
            angle = np.arccos(angle) / 3.14 * 180
            if angle < 160:
                str_guester = "9"
            else:
                str_guester = "1"

        elif len(up_fingers) == 2 and up_fingers[0] == 8 and up_fingers[1] == 20:
            str_guester = "ROCK"

        elif len(up_fingers) == 2 and up_fingers[0] == 8 and up_fingers[1] == 12:
            str_guester = "2"

        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 20:
            str_guester = "6"

        elif len(up_fingers) == 2 and up_fingers[0] == 4 and up_fingers[1] == 8:
            dis_3_6 = list_lms[3, :] - list_lms[6, :]
            dis_3_6 = np.sqrt(np.dot(dis_3_6, dis_3_6))
            dis_3_4 = list_lms[3, :] - list_lms[4, :]
            dis_3_4 = np.sqrt(np.dot(dis_3_4, dis_3_4))

            if dis_3_6  < dis_3_4:
                str_guester = "LOVE"
            else:
                str_guester = "8"

        elif len(up_fingers) == 3 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16:
            str_guester = "3"

        elif len(up_fingers) == 3 and up_fingers[0] == 4 and up_fingers[1] == 8 and up_fingers[2] == 12:
            str_guester = "7"

        elif len(up_fingers) == 4 and up_fingers[0] == 8 and up_fingers[1] == 12 and up_fingers[2] == 16 and \
                up_fingers[3] == 20:
            str_guester = "4"

        elif len(up_fingers) == 5:
            str_guester = "5"

        elif len(up_fingers) == 0:
            str_guester = "0"

        else:
            str_guester = ""

        return str_guester

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类
        self.slot_init()      #按钮初始化
    def slot_init(self):
        global Hand_gesture
        global Mouse_control
        Hand_gesture = False
        Mouse_control = False

        self.video_thread = HandThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.change_text_signal.connect(self.update_text)
        self.Gesture_btn.clicked.connect(self.gesture_btn_enable_on_click)
        self.Mouse_btn.clicked.connect(self.mouse_btn_enable_on_click)
    def gesture_btn_enable_on_click(self):
        global Hand_gesture
        global Mouse_control
        global Flip_sign
        Hand_gesture = True
        Mouse_control = False
        Flip_sign = True
        self.video_thread.start()
    def mouse_btn_enable_on_click(self):
        global Hand_gesture
        global Mouse_control
        global Flip_sign
        Hand_gesture = False
        Mouse_control = True
        Flip_sign = True
        self.video_thread.start()
    def update_image(self, image):
        self.camera.setPixmap(QPixmap.fromImage(image))
    def update_text(self, TextImage):
        self.results.setPixmap(QPixmap.fromImage(TextImage))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())