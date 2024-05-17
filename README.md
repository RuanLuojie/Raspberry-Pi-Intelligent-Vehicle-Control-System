# Raspberry-Pi-智慧車輛控制系統

## 專案描述
本專案旨在開發一個智慧小車系統，利用ASP.NET和Python API來實現網頁控制和影像串流服務，提供更便捷的使用體驗，避免市面上需下載軟體才能使用的繁瑣步驟。

## 專案目標
透過網頁進行控制和影像串流服務，以取代市面上需下載軟體才能使用的缺點，實現更方便、更直觀的智慧小車操作。

## 功能列表
- Raspberry Pi API控制
- MJPG影像串流伺服器
- ASP.NET Web後端
- ASP.NET API
- ChatGPT智慧助理
- 語音助理
- YOLOv5口罩辨識

## 系統需求
- ReSpeaker Mic Array 陣列麥克風
- 樹莓派3 (Raspberry Pi 3)
- Arduino Uno
- 伺服馬達
- WebCam

## 安裝指南

### Raspberry Pi
1. 創建專案資料夾並安裝Python專案：
    ```sh
    mkdir /home/pi/Desktop/Raspberry-Pi-Intelligent-Vehicle-Control-System
    cd /home/pi/Desktop/Raspberry-Pi-Intelligent-Vehicle-Control-System
    ```
2. 創建虛擬環境並啟動：
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
3. 安裝所需的Python模組：
    ```sh
    pip install -r requirements.txt
    ```
4. 執行專案：
    ```sh
    python main.py
    ```
   如果出現`alsa lib pcm.c:2660:(snd_pcm_open_noupdate) unknown pcm cards.pcm.front`錯誤，請使用以下命令：
    ```sh
    python main.py 2>/dev/null
    ```

### 電腦
1. 安裝Visual Studio (https://visualstudio.microsoft.com/zh-hant/downloads/)
2. 選擇`Visual Studio Community`並安裝`ASP.NET Core`，在安裝套件部分選擇`ASP.NET Core`，並選擇`.NET 6.0執行階段(長期支援)`或更高版本。
3. 打開專案檔案：
    ```sh
    Raspberry-Pi-Intelligent-Vehicle-Control-System>RasPi_IVControl>RasPi_IVControl.sln
    ```

## 使用說明

### Raspberry Pi
1. 修改`config.py`文件：
    ```python
    ARDUINO_PORT = "/dev/ttyACM0"  # Arduino端口
    VIDEO_SRC = 0  # 攝影機號碼
    SERVER_HOST = '0.0.0.0'  # 服務器主機地址
    SERVER_PORT = 7024  # 服務器端口號
    history_path = 'history.json'  # GPT歷史數據文件路徑
    api_key = ''  # GPT API密鑰
    ```

2. 如果找不到Arduino端口，請使用以下步驟：
    - 安裝Arduino軟體：
        ```sh
        sudo apt install arduino
        ```
    - 啟動Arduino軟體：
        ```sh
        arduino
        ```
    - 打開終端機，輸入以下命令查找Arduino端口：
        ```sh
        ls /dev/tty*
        ```
      你應該會看到一個名為`/dev/ttyACM`或`/dev/ttyUSB`的設備，這就是你的Arduino端口。

### ASP.NET
1. 更改API的IP地址：
    ```csharp
    // CarcontrolController.cs
    var raspberryPiUrl = "http://<你的RaspberryPi的IP>:7024/arduino_command";
    ```
   將`<你的RaspberryPi的IP>`替換為你實際的Raspberry Pi IP地址。

2. 更改接收API的IP地址：
    ```html
    <!-- Camera.html -->
    http://<你的RaspberryPi的IP>:8080/?action=stream
    ```
   將`<你的RaspberryPi的IP>`替換為你實際的Raspberry Pi IP地址。

3. 更改IP地址：
    ```javascript
    // Camera.js 和 home.js
    http://<你的RaspberryPi的IP>:8080/?action=stream
    http://<你的RaspberryPi的IP>:5000/video_feed
    ```
   將`<你的RaspberryPi的IP>`替換為你實際的Raspberry Pi IP地址。

### MaskDetect
1. 修改`main copy.py`文件：
    ```python
    cap = cv2.VideoCapture('http://<你的RaspberryPi的IP>:8080/?action=stream')
    ```
   將`<你的RaspberryPi的IP>`替換為你實際的Raspberry Pi IP地址。

2. 更改API的IP地址：
    ```python
    url = 'http://<你的電腦的IP>:7024/api/detection'
    ```
   將`<你的電腦的IP>`替換為你實際的電腦IP地址。

3. 啟動口罩辨識：
    ```sh
    python main copy.py
    ```
