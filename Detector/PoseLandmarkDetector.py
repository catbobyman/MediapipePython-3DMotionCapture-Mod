import mediapipe as mp
from mediapipe.tasks import python
import cv2
from mediapipe.tasks.python import vision
#  PoseLandmarkDetector 类
#  livestream模式
class PoseLandmarkDetector:
    def __init__(self,controller, model_path: str):
        self.BaseOptions = mp.tasks.BaseOptions
        self.PoseLandmarker = mp.tasks.vision.PoseLandmarker
        self.PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        self.PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.controller = controller

        options = self.PoseLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=model_path),
            running_mode=self.VisionRunningMode.LIVE_STREAM,

            result_callback=self.print_result_pose
        )

        self.landmarker = self.PoseLandmarker.create_from_options(options)

    def print_result_pose(self,result, output_image: mp.Image, timestamp_ms: int):
        self.controller.get_result_pose(result,timestamp_ms)
        # if result:
        #     print(result.pose_world_landmarks)





    def detect_live_pose(self):


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
#     modelpath='../Models/pose_landmarker_full.task'
#     posedetector =PoseLandmarkDetector(modelpath)
#     posedetector.detect_live_pose()
#     posedetector.landmarker.detect_async()

