# -*- coding: utf-8 -*-


import asyncio
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import io
from config import *
from mood import Voice as Va
from mood.Chat import ChatAssistant
import serial
from aiohttp import web
import psutil

current_directory = os.path.dirname(__file__)
chat_file_path = os.path.join(current_directory, history_path)

class RaspberryPi:
    def __init__(self, chat_file_path, api_key):
        self.voiceAssistant = Va.VoiceAssistant()
        self.chatAssistant = ChatAssistant(chat_file_path, api_key)
        self.ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
        print("Serial port opened")

    def get_cpu_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            if 'cpu_thermal' in temps:
                return temps['cpu_thermal'][0].current
            else:
                return None
        except (KeyError, IndexError, AttributeError):
            return None

    async def speech_function(self):
        while True:
            try:
                voice_text = await self.voiceAssistant.voiceInput()
                if voice_text:
                    print(f"Detected voice input: {voice_text}")
                    if "志航" in voice_text:
                        response_text = await self.chatAssistant.interact(voice_text)
                        print(response_text)
                        await self.play_audio(response_text)
            except Exception as e:
                print(f"Error in speech function: {e}")

    async def play_audio(self, text):
        tts = gTTS(text=text, lang="zh-cn")
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        play(audio)

    async def handle_arduino_command(self, request):
        data = await request.json()
        command = data.get('command', '')

        try:
            self.ser.write(command.encode())
            cpu_temp = self.get_cpu_temperature()
            if cpu_temp is not None:
                print(f"Received command: {command}, CPU Temperature: {cpu_temp:.2f}C")
            else:
                print(f"Received command: {command}, CPU Temperature: Could not read")
            return web.Response(text=f"Arduino command '{command}' executed.")
        except Exception as e:
            print(f"Error sending command: {e}")
            return web.Response(text=str(e), status=500)

    def setup_routes(self, app):
        app.router.add_post('/arduino_command', self.handle_arduino_command)

    def on_cleanup(self, app):
        self.ser.close()
        print("Serial port closed")

    def create_app(self):
        app = web.Application()
        self.setup_routes(app)
        app.on_cleanup.append(self.on_cleanup)
        return app

async def main():
    pi = RaspberryPi(chat_file_path, api_key)

    app = pi.create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, SERVER_HOST, SERVER_PORT)

    await asyncio.gather(pi.speech_function(), site.start())

if __name__ == "__main__":
    asyncio.run(main())
