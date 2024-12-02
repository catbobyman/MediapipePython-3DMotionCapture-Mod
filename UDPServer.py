import socket
import threading
import queue
import os
import signal
import orjson
import time

import config
from ResultToJson import Handlandmark

#使用queue来作为缓冲
class UDPServer:
    def __init__(self, host=config.IP, port=config.PORT):
        # 初始化服务器的主机地址和端口号
        self.host = host
        self.port = port
        # 创建一个UDP套接字
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 服务器地址（主机和端口）
        self.address = (host, port)
        # 创建一个队列用于保存待发送的数据
        self.queue = queue.Queue()
        # 标识服务器是否正在运行
        self.is_running = False

    def start_server(self):
        # try:
        #     # 绑定套接字到指定地址和端口
        #     self.sock.bind(self.address)
        # except OSError as e:
        #     # 如果地址已被占用，则尝试杀死占用该端口的进程
        #     if "Address already in use" in str(e):
        #         self.kill_port_process()
        #         self.sock.bind(self.address)

        # 设置服务器运行状态为True
        self.is_running = True
        # 创建并启动一个线程来处理队列中的数据
        threading.Thread(target=self.process_queue).start()
        # while not self.queue.empty():
        #     print(self.queue.get())
        while self.queue.empty():
            print("Queue is empty")
        print(f"UDP Server started at {self.host}:{self.port}")

    def stop_server(self):
        # 停止服务器
        self.is_running = False
        # 关闭套接字
        self.sock.close()
        print("UDP Server stopped.")

    def kill_port_process(self):
        # 查找并杀死占用指定端口的进程
        pid_list = os.popen(f"lsof -t -i:{self.port}").read().split()
        for pid in pid_list:
            os.kill(int(pid), signal.SIGKILL)
        print(f"Killed process using port {self.port}")

    def send_data(self, data):
        # 将数据放入队列中
        try:
            # 尝试发送数据，如果没有客户端接收则忽略异常
            self.queue.put(data)
            # print(f"Sent {data}")
        except Exception as e:
            # 捕获并打印发送数据时的异常，避免阻塞摄像头操作
            print(f"Warning: Failed to send data: {e}")

    def process_queue(self):
        # 处理队列中的数据并发送到客户端
        while self.is_running:
            try:
                # 从队列中获取数据，超时时间为1秒
                data = self.queue.get()
                # print(data)
                # 通过UDP套接字发送数据
                self.sock.sendto(data, self.address)
                print(f"Sent data to {self.address}")
            except self.queue.empty():
                # 如果队列为空，则继续循环
                continue
            except Exception as e:
                # 捕获并打印发送数据时的异常
                print(f"Error while sending data: {e}")

    def run(self):
        # 启动服务器
        self.start_server()
        try:
            # 服务器运行时保持循环
            while self.is_running:
                time.sleep(0.05)
        except KeyboardInterrupt:
            # 捕获键盘中断，停止服务器
            self.stop_server()

# 示例用法
if __name__ == "__main__":
    udp_server = UDPServer()
    udp_server.start_server()

    # 创建并在单独的线程中发送示例JSON数据
    def generate_data():
        # 创建Handlandmark对象并添加手部的世界坐标
        hand = Handlandmark("left")
        hand.add_world_landmarks([type('lm', (object,), {'x': 0.1, 'y': 0.2, 'z': 0.3})() for _ in range(21)])
        while True:
            # 将Handlandmark对象转换为JSON格式的数据
            json_data = hand.to_json()
            # 发送数据到UDP服务器
            udp_server.send_data(json_data)
            time.sleep(0.05)  # 模拟实时数据生成

    # 启动数据生成线程
    data_thread = threading.Thread(target=generate_data)
    data_thread.start()

    try:
        # 运行服务器
        udp_server.run()
    except KeyboardInterrupt:
        # 捕获键盘中断，停止服务器
        udp_server.stop_server()
