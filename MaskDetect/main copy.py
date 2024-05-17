import torch
import cv2
from flask import Flask, Response
import numpy as np
import requests

# 载入模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'MaskDetect\best.pt')

app = Flask(__name__)

def send_detection_result(label, confidence, x1, y1, x2, y2):
    url = 'http://192.168.0.13:7024/api/detection'
    data = {
        'Label': label,
        'Confidence': float(confidence),  # 确保数据是 float 类型
        'X1': float(x1),
        'Y1': float(y1),
        'X2': float(x2),
        'Y2': float(y2)
    }
    response = requests.post(url, json=data)
    return response.status_code

def generate_frames():
    cap = cv2.VideoCapture('http://192.168.0.111:8080/?action=stream')
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 进行推论
        results = model(frame)
        
        # 绘制结果并发送到 ASP.NET Core API
        for result in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = result
            if conf < 0.79:
                label = 'NoMask'
                conf = 1 - conf  # 将信心指数调整为合理值以避免冲突
            else:
                label = 'Mask'
            send_detection_result(label, conf, x1, y1, x2, y2)
            
            color = (0, 255, 0) if label == 'Mask' else (0, 0, 255)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # 将影像转换为JPEG格式
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
