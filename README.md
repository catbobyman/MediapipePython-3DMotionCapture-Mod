
# MediapipePython-3DMotionCapture-Mod

[![GitHub repo](https://img.shields.io/badge/Repository-Link-blue)](https://github.com/catbobyman/MediapipePython-MotionTracking-Mod?tab=readme-ov-file)

## 简介

**MediapipePython-3DMotionCapture-Mod** 是一个基于 Mediapipe 和 Python 的运动追踪模块，旨在通过自定义实现更高效的运动数据捕获和处理。此项目为开发虚拟主播、实时动作捕捉等领域提供了极大的便利。

---

## 功能

- **高效数据管理**：通过 `DataController.py` 进行捕获数据的集中化处理。
- **支持 JSON 输出**：`ResultToJson.py` 提供运动数据的 JSON 格式输出。
- **UDP 通信支持**：通过 `UDPServer.py` 和 `UDPServer_direct.py` 实现网络通信。
- **可视化工具**：`VisualUtilities.py` 提供了可视化和调试工具。
- **模型与检测集成**：项目包含 `Models` 和 `Detector` 文件夹，用于处理核心检测和模型。

---

## 项目结构

```
MediapipePython-MotionTracking-Mod/
├── Detector/             # 检测的脚本
    ├── FaceLandmarkDetector.py 
    └── PoseLandmarkDetector.py 
    └── HandLandmarkDetector.py
    └── HandLandmarkDetector_New.py
├── Models/               # 存储模型
    ├── face_landmarker_v2_with_blendshapes.task    
    └── hand_landmarker.task 
    └── pose_landmarker_full.task
├── .gitattributes       
├── DataController.py     
├── LICENSE               
├── ResultToJson.py       # 数据转换为 JSON
├── UDPServer.py          # UDP 通信模块
├── UDPServer_direct.py   # 直接式 UDP 通信模块
├── VisualUtilities.py    # 可视化工具
├── config.py             # 配置文件
├── main.py               # 主运行脚本
├── requirements.txt      # 项目依赖
```

---

## 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/catbobyman/MediapipePython-MotionTracking-Mod.git
cd MediapipePython-MotionTracking-Mod
```

### 2. 安装依赖
确保你已安装 Python 3.8+，然后运行以下命令：
```bash
pip install -r requirements.txt
```

### 3. 运行项目
运行主脚本：
```bash
python main.py
```

---

## 依赖

此项目依赖以下库，详见 `requirements.txt`：
- Mediapipe
- OpenCV
- NumPy
...

---

## 贡献

欢迎提交 Issue 和 Pull Request！如有任何建议，请联系 [catbobyman](https://github.com/catbobyman)。

---

## 开源协议

此项目基于 [MIT License](LICENSE) 开源。
