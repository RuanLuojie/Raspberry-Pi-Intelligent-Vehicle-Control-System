import serial
from aiohttp import web


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
print("Serial port opened")

async def handle_arduino_command(request):
    data = await request.json()
    command = data.get('command', '')

    try:
        ser.write(command.encode())
        print(f"Received command: {command}")
        return web.Response(text=f"Arduino command '{command}' executed.")
    except Exception as e:
        print(f"Error sending command: {e}")
        return web.Response(text=str(e), status=500)

def setup_routes(app):
    app.router.add_post('/arduino_command', handle_arduino_command)

def on_cleanup(app):
    ser.close()
    print("Serial port closed")

def create_app():
    app = web.Application()
    setup_routes(app)
    app.on_cleanup.append(on_cleanup)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=7024)  
