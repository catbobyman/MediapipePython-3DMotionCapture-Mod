import cv2
import numpy as np
import mediapipe as mp
import config
from DataController import DataController
from VisualUtilities import draw_facelandmarks_on_image,draw_handlandmarks_on_image,draw_poselandmarks_on_image,plot_face_blendshapes_bar_graph
from Detector.HandLandmarkDetector_New import HandLandmarkDetector_New,to_json
import os
import time


if __name__ == '__main__':

    controller = DataController()
    controller.start()  # 启动UDP服务器

    counter = 0  # 计算循环次数，计算处理速度用

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        # 记录每次迭代的开始时间
        loop_start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        # 获取当前帧的时间戳
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        # 异步检测帧
        controller.detect_async_frame(frame, timestamp_ms)
        #使用HandLandmarkDetector_new
        controller.detect_sync_frame(frame, timestamp_ms)

        #example(HandLandmarkDetector_new)：
        # #HandLan...._New不用本地模型，推理速度更快
        # # 手部检测+发送
        # frame, hand_results = hand_detector.process_frame(frame)
        # # 转换成json
        # json_handdata = to_json(hand_results)
        # # 发送
        # controller.udp_server.send_data(json_handdata)
        # #打印
        # print(json_handdata)



        #可视化

        if controller.face_results is not None:
            frame=draw_facelandmarks_on_image(frame,controller.face_results)


        if controller.pose_results is not None:
            frame=draw_poselandmarks_on_image(frame,controller.pose_results)


        # if controller.hand_results is not None:
        #     frame=draw_handlandmarks_on_image(frame,controller.hand_results)

        if controller.hand_results_new is not None:
            frame=controller.hand_detector_new.draw_hand_annotations(frame,controller.hand_results_new)

        #example(HandLandmarkDetector_new)：
        # if hand_results is not None:
        #     #新的手部注释方法
        #     frame=hand_detector.draw_hand_annotations(frame,hand_results)

        cv2.imshow('frame', frame)

        # 循环次数
        counter += 1
        # 记录每次迭代的结束时间
        loop_end_time = time.time()

        # 计算每次循环的执行时间
        loop_elapsed_time = loop_end_time - loop_start_time
        print(f"第 {counter} 次循环执行检测时间: {loop_elapsed_time:.5f} 秒")

        # 按下ESC键退出循环
        if cv2.waitKey(1) & 0xFF == 27:
            # 释放摄像头并停止UDPServer
            cap.release()
            controller.stop()
            cv2.destroyAllWindows()
            break






