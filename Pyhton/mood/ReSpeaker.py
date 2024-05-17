import serial
from tuning import Tuning
import usb.core
import usb.util
import time  # 确保导入 time 模块

class DirectionalMicrophoneController:
    def __init__(self, serial_port, baud_rate=9600):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
        if self.dev is None:
            raise ValueError("Device not found")
        self.mic_tuning = Tuning(self.dev)

    def process_direction(self):
        direction = self.mic_tuning.direction
        command = 'X'  # 默认不转向
        if -45 <= direction <= 45:
            command = 'X'  # 不转向
        elif 45 < direction <= 135:
            command = 'D'  # 向右转90度
        elif 135 < direction or direction <= -135:
            command = 'B'  # 转180度
        elif -135 < direction < -45:
            command = 'A'  # 向左转90度

        self.ser.write(command.encode('utf-8'))  # 发送命令到 Arduino
        print(f"Direction: {direction}°, Command: {command}")
        time.sleep(1)  # 延迟1秒
        self.ser.write('X'.encode('utf-8'))  # 发送停止命令到 Arduino
        print("Stop command sent.")

    def run(self):
        try:
            while True:
                self.process_direction()
        except KeyboardInterrupt:
            print("Interrupted")
            self.cleanup()

    def cleanup(self):
        self.ser.close()
        print("Serial connection closed.")
