import json
import datetime
import os
import io
from openai import OpenAI

class ChatAssistant:
    def __init__(self, filePath, apiKey):
        self.filePath = filePath
        self.apiKey = apiKey
        self.ensureFileExists()

    def ensureFileExists(self):
        if not os.path.exists(self.filePath):
            with open(self.filePath, "w", encoding='utf-8') as file:
                json.dump([], file)

    async def interact(self, userInput):
        try:
            conversationHistory = self.readConversationFromJson()
            conversationHistory = self.removeOldConversations(conversationHistory)
            conversationHistory.append({"role": "user", "content": userInput, "timestamp": self.getCurrentTimestamp()})

            conversationHistoryForApi = [{"role": msg["role"], "content": msg["content"]} for msg in conversationHistory]

            client = OpenAI(api_key=self.apiKey)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=conversationHistoryForApi, max_tokens=50, stream=False
            )

            modelResponse = response.choices[0].message.content
            conversationHistory.append({"role": "assistant", "content": modelResponse, "timestamp": self.getCurrentTimestamp()})
            self.writeConversationToJson(conversationHistory)
            
            print("GPT response:", modelResponse)  # 日志输出 GPT 的响应
            return modelResponse
        except Exception as e:
            print(f"An error occurred: {e}")

    def getCurrentTimestamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    def removeOldConversations(self, conversationHistory, maxHistoryLength=5, timeLimitMinutes=60):
        timeLimit = datetime.timedelta(minutes=timeLimitMinutes)
        timeThreshold = datetime.datetime.now() - timeLimit
        filteredMessages = [msg for msg in conversationHistory if "timestamp" in msg and datetime.datetime.fromisoformat(msg["timestamp"]) > timeThreshold]
        return filteredMessages[-maxHistoryLength:] if len(filteredMessages) > maxHistoryLength else filteredMessages

    def readConversationFromJson(self):
        with open(self.filePath, "r", encoding="utf-8") as file:
            return json.load(file)

    def writeConversationToJson(self, conversationHistory):
        with open(self.filePath, "w", encoding="utf-8") as file:
            json.dump(conversationHistory, file, ensure_ascii=False, indent=2)
