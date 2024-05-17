import torch
import cv2
from flask import Flask, Response, jsonify
import numpy as np
import requests

# 載入模型
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'MaskDetect\best.pt')

app = Flask(__name__)

def send_detection_result(label, confidence, x1, y1, x2, y2):
    url = 'http://192.168.0.13:7024/api/detection'
    data = {
        'Label': label,
        'Confidence': float(confidence),  # 確保數據是 float 類型
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
        
        # 進行推論
        results = model(frame)
        
        # 繪製結果並發送到 ASP.NET Core API
        for result in results.xyxy[0].cpu().numpy():
            x1, y1, x2, y2, conf, cls = result
            if conf < 0.79:
                label = 'NoMask'
            else:
                label = f'{model.names[int(cls)]} {conf:.2f}'
            send_detection_result(label, conf, x1, y1, x2, y2)
            
            color = (0, 255, 0) if label.startswith('Mask') else (0, 0, 255)
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # 將影像轉換為JPEG格式
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
