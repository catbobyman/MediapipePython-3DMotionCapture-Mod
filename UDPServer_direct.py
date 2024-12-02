# -*- coding: utf-8 -*-            
# @Author : catbobyman
# @Time : 2024/11/29 上午2:37
import socket
import json
import time
import os
import signal

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建UDP套接字

    def send_data(self, json_data):
        #发送数据到目标
        if self.running:
            try:
                self.sock.sendto(json_data, (self.host, self.port))  # 直接发送数据
                print(f"Sent to {self.host}:{self.port}")
            except Exception as e:
                print(f"Error while sending data: {e}")
        else:
            print("Server is not running. Data not sent.")

    def start(self):
        #启动UDPServer
        self.sock.bind(('', 0))  # 绑定一个随机端口
        self.running = True
        print(f"UDPServer_New started, sending to {self.host}:{self.port}")

    def stop_server(self):
        #停止UDPServer
        self.running = False
        self.sock.close()
        print("UDPServer_New stopped.")

    def kill_port_process(self):
        # 查找并结束占用端口的进程
        pid_list = os.popen(
            f"powershell -Command Get-NetTCPConnection -LocalPort {self.port} | Select-Object -ExpandProperty OwningProcess").read().split()
        for pid in pid_list:
            os.kill(int(pid), signal.SIGKILL)
        print(f"Killed process using port {self.port}")

#test
if __name__ == "__main__":
    udp_server = UDPServer('127.0.0.1', 8888)
    udp_server.kill_port_process()
    udp_server.start()

    # 模拟发送JSON数据
    for i in range(5):
        json_data = {"id": i, "message": f"Hello {i}"}
        json_data = json.dumps(json_data).encode('utf-8')
        udp_server.send_data(json_data)
        time.sleep(0.1)  # 等待1秒

    # 结束发送
    time.sleep(2)  # 给发送线程足够的时间发送数据
    udp_server.stop_server()
