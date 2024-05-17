import asyncio
import serial_asyncio
from serial.tools import list_ports


class ArduinoProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Data received:", data.decode())

    def connection_lost(self, exc):
        print("Connection lost:", exc)


class ArduinoConnector:
    def __init__(self, loop):
        self.port = None
        self.loop = loop
        self.transport = None
        self.protocol = None

    async def find_port(self):
        arduino_ports = [
            p.device for p in list_ports.comports() if "Arduino" in p.description
        ]
        try:
            return arduino_ports[0]
        except IndexError:
            return None

    async def connect(self):
        self.port = await self.find_port()
        if self.port is None:
            print("No Arduino port found.")
            return

        try:
            self.transport, self.protocol = (
                await serial_asyncio.create_serial_connection(
                    self.loop, ArduinoProtocol, self.port, baudrate=9600
                )
            )
            print(f">> Connected to Arduino on {self.port} <<")
            return self.port
        except Exception as e:
            print(f"Failed to connect to Arduino port: {e}")
            return None

    def send(self, command):
        if self.transport:
            self.transport.write(command.encode())
            print(f"Command sent: {command}")
        else:
            print("Connection is not established.")


async def main():
    loop = asyncio.get_running_loop()
    arduino = ArduinoConnector(loop)
    await arduino.connect()
    arduino.send("Your command here")

if __name__ == "__main__":
    asyncio.run(main())
