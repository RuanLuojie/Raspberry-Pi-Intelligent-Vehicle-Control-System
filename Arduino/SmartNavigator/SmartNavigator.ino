#include <WiFi.h>
#include <esp_camera.h>
#include <WebServer.h> // HTTP伺服器庫

// Wi-Fi 設置
const char* ssid = "nga";          // WiFi 名稱
const char* password = "0958188700";  // WiFi 密碼

// 攝影機引腳配置（AI Thinker 模組）
#define PWDN_GPIO_NUM    -1
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27
#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      21
#define Y4_GPIO_NUM      19
#define Y3_GPIO_NUM      18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22

WebServer server(80); // HTTP伺服器，監聽80埠

// 初始化攝影機
bool setupCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_QVGA; // 測試用解析度
    config.jpeg_quality = 10;          // 壓縮品質
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_CIF;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }
  Serial.println("Camera init successful");
  return true;
}

// Wi-Fi 連接
void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // 等待連接成功
  int retry_count = 0;
  while (WiFi.status() != WL_CONNECTED && retry_count < 20) {
    delay(1000);
    Serial.print(".");
    retry_count++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }
}

// 提供攝影機影像串流
void handleStream() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    server.send(500, "text/plain", "Camera capture failed");
    return;
  }

  server.setContentLength(fb->len);
  server.send(200, "image/jpeg");
  server.sendContent((const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

// 設置 HTTP 路由
void setupServer() {
  server.on("/", []() {
    server.send(200, "text/plain", "ESP32-CAM is running. Access /stream for image.");
  });
  server.on("/stream", handleStream);
  server.begin();
  Serial.println("HTTP server started");
}

void setup() {
  Serial.begin(115200);

  // Wi-Fi 連接
  connectToWiFi();

  if (WiFi.status() == WL_CONNECTED) {
    // 初始化攝影機
    if (setupCamera()) {
      // 設置 HTTP API
      setupServer();
    } else {
      Serial.println("Failed to initialize camera. HTTP server not started.");
    }
  }
}

void loop() {
  server.handleClient(); // 處理 HTTP 請求
}
