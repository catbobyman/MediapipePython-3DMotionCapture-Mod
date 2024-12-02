import mediapipe as mp
import cv2


#  FaceLandmarkDetector 类;
#  livestream模式
class FaceLandmarkDetector:
    def __init__(self, controller,model_path: str):
        self.BaseOptions = mp.tasks.BaseOptions
        self.FaceLandmarker = mp.tasks.vision.FaceLandmarker
        self.FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        self.FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        self.controller = controller

        options = self.FaceLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=model_path),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            output_face_blendshapes=True,
            num_faces=1,
            result_callback=self.print_result_face)

        self.landmarker = self.FaceLandmarker.create_from_options(options)

    def print_result_face(self,result, output_image: mp.Image, timestamp_ms: int):
        self.controller.get_result_face(result,timestamp_ms)

        # 只需要faceblendshapes的数据
        # if result.face_blendshapes:
        #
        #     print('face blendshapes: {}'.format(result.face_blendshapes))

    def detect_live_face(self):


        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 将帧转换为 MediaPipe 图像对象
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))

            # livestream模式下的detect方法(detect_async)：异步执行面部标志点检测
            self.landmarker.detect_async(mp_image, timestamp_ms)

        cap.release()



# test
# if __name__ == "__main__":
#     modelpath='../Models/face_landmarker.task'
#     facedetector = FaceLandmarkDetector(modelpath)
#     facedetector.detect_live_face()

