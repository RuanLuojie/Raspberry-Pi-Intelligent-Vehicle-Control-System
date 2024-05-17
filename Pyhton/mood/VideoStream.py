import cv2
from aiohttp import web

video = cv2.VideoCapture(0)  

async def generate_frames():
    while True:
        ret, frame = video.read()
        if not ret:
            break  
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    return

async def video_feed(request):
    response = web.StreamResponse()
    response.content_type = 'multipart/x-mixed-replace; boundary=frame'
    await response.prepare(request)
    try:
        async for data in generate_frames():
            await response.write(data)
    except ConnectionResetError:
        print("Connection was closed by client.")
    finally:
        video.release()  
    return response

def setup_routes(app):
    app.router.add_get('/video', video_feed)

app = web.Application()
setup_routes(app)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)  
