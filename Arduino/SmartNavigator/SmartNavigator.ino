#include <Servo.h>

Servo servomotorL; // 左馬達
Servo servomotorR; // 右馬達

const int servoPinL = 13; // 左馬達控制引腳
const int servoPinR = 12; // 右馬達控制引腳

const int pingPin1 = 10; // 超聲波模塊1的引腳
const int pingPin2 = 11; // 超聲波模塊2的引腳

int motorL = 93; // 左馬達初始位置
int motorR = 93; // 右馬達初始位置

unsigned long previousMillis = 0; // 上次讀取超聲波距離的時間
const long interval = 500; // 讀取超聲波距離的間隔時間

void setup() {
  servomotorL.attach(servoPinL); // 將左馬達連接到相應的控制引腳
  servomotorR.attach(servoPinR); // 將右馬達連接到相應的控制引腳
  Serial.begin(9600); // 初始化串行通信
}

void loop() {
  unsigned long currentMillis = millis();

  // 每隔一段時間讀取超聲波距離並輸出
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    readAndPrintUltraSonicDistance();
  }

  // 監聽串行通信是否有命令傳入
  if (Serial.available() > 0) {
    char command = Serial.read(); // 讀取傳入的命令
    processCommand(command); // 處理接收到的命令
  }
}

// 讀取超聲波距離並輸出到串口
void readAndPrintUltraSonicDistance() {
  int R = pingSensor(pingPin1); // 讀取超聲波模塊1的距離
  int L = pingSensor(pingPin2); // 讀取超聲波模塊2的距離

  // 將距離輸出到串口
  Serial.print(R);
  Serial.print(",");
  Serial.print(L);
  Serial.println();
}

// 讀取超聲波距離
int pingSensor(int pingPin) {
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2); // 發送一個短脈衝
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5); // 發送一個長脈衝
  digitalWrite(pingPin, LOW);
  pinMode(pingPin, INPUT);
  long duration = pulseIn(pingPin, HIGH); // 計算超聲波從發射到接收的時間
  return duration / 2 / 29; // 將時間轉換為距離（單位：厘米）
}

// 處理接收到的命令並控制馬達運動
void processCommand(char command) {
  int speedChange = 5; // 馬達速度變化量

  // 根據接收到的命令執行相應的操作
  switch (command) {
    case 'A': // 向左轉
      motorL = max(motorL - speedChange, 0); // 左馬達逆時針轉動
      motorR = min(motorR - (speedChange * 2), 180); // 右馬達順時針轉動
      break;
    case 'D': // 向右轉
      motorL = min(motorL + (speedChange * 2), 180); // 左馬達順時針轉動
      motorR = max(motorR + speedChange, 0); // 右馬達逆時針轉動
      break;
    case 'W': // 向前
      motorL = min(motorL + speedChange, 100); // 左馬達順時針轉動
      motorR = max(motorR - speedChange, 0); // 右馬達逆時針轉動
      break;
    case 'S': // 向後
      motorL = max(motorL - speedChange, 0); // 左馬達逆時針轉動
      motorR = min(motorR + speedChange, 180); // 右馬達順時針轉動
      break;
    case 'X': // 停止
      motorL = 93; // 左馬達停止
      motorR = 93; // 右馬達停止
      break;
  }

  servomotorL.write(motorL); // 控制左馬達運動
  servomotorR.write(motorR); // 控制右馬達運動
}
