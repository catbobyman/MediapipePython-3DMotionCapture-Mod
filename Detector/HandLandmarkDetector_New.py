import cv2
import mediapipe as mp
from ResultToJson import Handlandmark
import threading

class HandLandmarkDetector_New:
    def __init__(self,controller,  model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # 初始化 MediaPipe 的 hand 模块和绘图工具
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.controller=controller
        self.result_callback = controller.get_resluts_hands_new  # Store the callback

    def process_frame(self, image):
        # 将图像标记为不可写，以提高性能
        image.flags.writeable = False
        # 将图像从 BGR 转换为 RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 使用 hand 模块处理图像，检测手部
        results = self.hands.process(image)

        # If a callback is provided, invoke it with the results
        if self.result_callback:
            self.result_callback(results)

        return image, results

    def draw_hand_annotations(self, image, results):
        # 在图像上绘制手部注释
        image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )


        return image

    def print_hand_info(self, results):
        # 打印手的世界坐标和手性信息
        if results.multi_hand_world_landmarks and results.multi_handedness:
            for hand_no, (hand_world_landmarks, handedness) in enumerate(zip(results.multi_hand_world_landmarks, results.multi_handedness)):
                label = handedness.classification[0].label  # "Left" 或 "Right"
                print(f"Hand {hand_no + 1} ({label}):")
                for idx, landmark in enumerate(hand_world_landmarks.landmark):
                    print(f"  World Landmark {idx}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")

def to_json(results):
    # 将手部信息转换为 JSON 格式的数据
    if results.multi_hand_world_landmarks and results.multi_handedness:
        for hand_world_landmarks, handedness in zip(results.multi_hand_world_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # "Left" 或 "Right"
            hand = Handlandmark(label)
            hand.add_world_landmarks(hand_world_landmarks.landmark)
            return hand.to_json()
    return None



def handle_hand_landmarks(results):
    # 结果回调处理函数
    json_data = to_json(results)
    if json_data:
        print("Hand landmarks JSON:", json_data)
    else:
        print("No hand landmarks detected.")

#test:
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    hand_detector = HandLandmarkDetector_New(result_callback=handle_hand_landmarks)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # 处理每一帧，检测手部
        image, results = hand_detector.process_frame(image)
        # 在图像上绘制手部注释
        image = hand_detector.draw_hand_annotations(image, results)

        # 水平翻转图像以进行自拍视图显示
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # 释放摄像头并关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()
