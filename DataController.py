import mediapipe as mp
import cv2
import config
from ResultToJson import Handlandmark,Faceblendshape,Poselandmark,Facelandmark
from Detector.PoseLandmarkDetector import PoseLandmarkDetector
from Detector.FaceLandmarkDetector import FaceLandmarkDetector
from Detector.HandLandmarkDetector import HandLandmarkDetector
from Detector.HandLandmarkDetector_New import HandLandmarkDetector_New,to_json
import threading
#直接发送
from UDPServer_direct import UDPServer
#使用queue来作为缓冲
# from UDPServer import UDPServer


class DataController:
    def __init__(self):
        self.hand_detector = HandLandmarkDetector(self,config.HAND_MODEL)
        self.face_detector = FaceLandmarkDetector(self,config.FACE_MODEL)
        self.pose_detector = PoseLandmarkDetector(self,config.POSE_MODEL)
        self.hand_detector_new=HandLandmarkDetector_New(self)
        #初始化result,用来可视化
        self.face_results=None
        self.hand_results=None
        self.pose_results=None
        self.hand_results_new=None
        self.face_blendshapes_for_visualization=None
        # 初始化UDP服务器
        self.udp_server = UDPServer(config.IP,config.PORT)
        self.udp_server.kill_port_process()

        # #
        # self.udp_server_new = UDPServer_New(config.IP,config.PORT)


    def start(self):

        # 启动UDP服务器线程
        # threading.Thread(target=self.udp_server.run, daemon=True).start()  # 将 UDPServer 的启动线程设为守护线程(#使用queue来作为缓冲)
        self.udp_server.start()#直接发送（UDPServer）



    def stop(self):
        # 停止UDP服务器
        self.udp_server.stop_server()



    def detect_async_frame(self, frame,timestamp_ms):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        #旧版的更新手部

        # self.hand_detector.landmarker.detect_async(mp_image,timestamp_ms)
        self.face_detector.landmarker.detect_async(mp_image,timestamp_ms)
        self.pose_detector.landmarker.detect_async(mp_image,timestamp_ms)

    #不使用使用模型
    def detect_sync_frame(self, frame,timestamp_ms):
        self.hand_detector_new.process_frame(frame)


    def get_result_hands(self,result,timestamp_ms):#回调使用
        self.hand_results=result


        for i in range(len(result.handedness)):
            self.left_hand=Handlandmark("left")
            self.right_hand=Handlandmark("right")

            if result.handedness[i][0].category_name == 'Left':
                self.left_hand.add_world_landmarks(result.hand_world_landmarks[i])
                self.json_hand=self.left_hand.to_json()
                print(self.json_hand)
                # 发送手部JSON数据到UDP服务器
                self.udp_server.send_data(self.json_hand)

            else:
                self.right_hand.add_world_landmarks(result.hand_world_landmarks[i])
                self.json_hand=self.right_hand.to_json()
                print(self.json_hand)
                # 发送手部JSON数据到UDP服务器
                self.udp_server.send_data(self.json_hand)

    def get_result_face(self,result,timestamp_ms):#回调使用
        self.face_results=result
        self.face_blendshapes_for_visualization=result.face_blendshapes
        if result is not None and len(result.face_blendshapes) > 0:
            self.face_blendshapes=Faceblendshape()
            self.face_blendshapes.add_face_blendshape(result.face_blendshapes[0])
            self.json_face_blendshapes=self.face_blendshapes.to_json()
            print(self.json_face_blendshapes)
            # 发送面部JSON数据到UDP服务器
            self.udp_server.send_data(self.json_face_blendshapes)

        if result is not None and len(result.face_landmarks)>0:
            self.face_landmarks=Facelandmark()
            self.face_landmarks.add_face_landmarks(result.face_landmarks[0])
            self.json_face_landmarks=self.face_landmarks.to_json()
            print(self.json_face_landmarks)
            self.udp_server.send_data(self.json_face_landmarks)



    def get_result_pose(self,result,timestamp_ms):#回调使用
        self.pose_results=result
        if result is not None and len(result.pose_world_landmarks) > 0:
            self.pose_data=Poselandmark()
            self.pose_data.add_world_landmarks(result.pose_world_landmarks[0])
            self.json_pose=self.pose_data.to_json()
            print(self.json_pose)
            # 发送姿势JSON数据到UDP服务器
            self.udp_server.send_data(self.json_pose)

    # 不使用使用模型，回调使用
    def get_resluts_hands_new(self,result):

            self.hand_results_new=result
            json_hand_data=to_json(self.hand_results_new)
            print(json_hand_data)
            ## 发送姿势JSON数据到UDP服务器
            self.udp_server.send_data(json_hand_data)

#test:
if __name__ == '__main__':
    controller = DataController()
    controller.start()

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # 获取当前帧的时间戳
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        # 异步检测帧
        controller.detect_async_frame(frame, timestamp_ms)
        # 使用HandLandmarkDetector_new
        controller.detect_sync_frame(frame, timestamp_ms)
    controller.stop()




