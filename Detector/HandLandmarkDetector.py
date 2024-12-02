import mediapipe as mp

import cv2

#  PoseLandmarkDetector 类
#  livestream模式
class HandLandmarkDetector:
    def __init__(self,controller, model_path: str):
        self.BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.controller = controller

        options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=model_path),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.3,
            min_tracking_confidence=0.3,
            num_hands=2,
            result_callback=self.print_result_hands
        )

        self.landmarker = self.HandLandmarker.create_from_options(options)

    def print_result_hands(self,result, output_image: mp.Image, timestamp_ms: int):

        self.controller.get_result_hands(result,timestamp_ms)


        # for i in range(len(result.handedness)):
        #
        #     if result.handedness[i][0].category_name == 'Left':
        #         for lm in result.hand_world_landmarks[i]:
        #             print(lm.x)
        #         # print(result.handedness[1][0].category_name)
        #
        #
        #     else:
        #         for lm in result.hand_world_landmarks[i]:
        #             print(lm.x)
        #         # print(result.handedness[i][0].category_name)


        # print(result.handedness+result.hand_world_landmarks)



    def detect_live_hands(self):


        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 将帧转换为 MediaPipe 图像对象
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

            # livestream模式下的detect方法(detect_async)：异步执行面部标志点检测
            self.landmarker.detect_async(mp_image,timestamp_ms)

        cap.release()



# test
# if __name__ == "__main__":
#
#     modelpath='../Models/hand_landmarker.task'
#     handsdetector =HandLandmarkDetector( modelpath)
#     handsdetector.detect_live_hands()
