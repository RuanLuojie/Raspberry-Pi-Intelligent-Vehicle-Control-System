# -*- coding: utf-8 -*-
import serial
from aiohttp import web
import psutil

# Open the serial port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
print("Serial port opened")

# Function to get CPU temperature
def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'cpu_thermal' in temps:
            return temps['cpu_thermal'][0].current
        else:
            return None
    except (KeyError, IndexError, AttributeError):
        return None

# Handler for Arduino command
async def handle_arduino_command(request):
    data = await request.json()
    command = data.get('command', '')

    try:
        ser.write(command.encode())
        cpu_temp = get_cpu_temperature()
        if cpu_temp is not None:
            return(f"Received command: {command}, CPU Temperature: {cpu_temp:.2f}C")
        else:
            return(f"Received command: {command}, CPU Temperature: Could not read")
        return web.Response(text=f"Arduino command '{command}' executed.")
    except Exception as e:
        print(f"Error sending command: {e}")
        return web.Response(text=str(e), status=500)

# Setup routes
def setup_routes(app):
    app.router.add_post('/arduino_command', handle_arduino_command)

# Cleanup function to close the serial port
def on_cleanup(app):
    ser.close()
    print("Serial port closed")

# Create the app
def create_app():
    app = web.Application()
    setup_routes(app)
    app.on_cleanup.append(on_cleanup)
    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=7024)
    
