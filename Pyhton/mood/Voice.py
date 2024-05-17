import asyncio
import speech_recognition as sr
import sys

class VoiceAssistant:
    
    def __init__(self):
        self.text = ""

    async def voiceInput(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)  # 自動調整環境噪音
            print("請準備開始說話...")

            try:
                # 開始異步監聽
                audio_future = asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: recognizer.listen(source, phrase_time_limit=6)
                )
                
                # 錄音倒計時，倒計時期間保持監聽
                for remaining in range(7, 0, -1):
                    sys.stdout.write(f"\r錄音中... (剩餘 {remaining}s)   ")
                    sys.stdout.flush()
                    await asyncio.sleep(1)

                # 等待異步監聽結果
                audio = await audio_future  # 此處獲取到的是真正的audio對象
                
                # 開始異步識別
                result_future = asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: recognizer.recognize_google(audio, language="zh-TW")  # 此處傳遞audio對象
                )
                self.text = await result_future
                print(f"\n識別結果: {self.text}")
                return self.text
                
                
            except sr.WaitTimeoutError:
                print("\r監聽超時，請再試一次。          ")
            except sr.UnknownValueError:
                print("\r無法識別您的語音。          ")
            except sr.RequestError as e:
                print(f"\r請求錯誤; {e}")
            except Exception as e:
                print(f"\r錯誤：{e}")

async def main():
    va = VoiceAssistant()
    await va.voiceInput()

if __name__ == "__main__":
    asyncio.run(main())
