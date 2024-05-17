#mood/CarAPI.py
import aiohttp
from aiohttp import web
import cv2
import asyncio
import serial
from config import *

video = cv2.VideoCapture(0)

async def generate_frames():
    while True:
        ret, frame = video.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

async def video_feed(request):
    response = web.StreamResponse()
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'

    await response.prepare(request)
    async for data in generate_frames():
        await response.write(data)

    return response

async def handle_arduino_command(request):
    data = await request.json()
    command = data.get('command')
    if command and ARDUINO_PORT:
        with serial.Serial(ARDUINO_PORT, 9600, timeout=1) as ser:
            ser.write((command + '\n').encode())
        return web.Response(text=f"Arduino 命令 '{command}' 已處理。")
    return web.Response(text="請求中沒有包含有效指令，或者 Arduino 串口未設置。")

app = web.Application()
app.router.add_get('/video', video_feed)
app.router.add_post('/arduino_command', handle_arduino_command)

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=7024)
    await site.start()
    await asyncio.Event().wait()  # Keep running until interrupted

if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.new_event_loop())  # Ensure the new loop for the main process
    asyncio.get_event_loop().run_until_complete(main())
