using Microsoft.AspNetCore.Mvc;

namespace RasPi_IVControl.Controllers
{
    [ApiController] // 表示這是一個API控制器
    [Route("api/[controller]")] // 設定路由前綴，自動使用控制器名稱作為路由
    public class CommandController : ControllerBase
    {
        private readonly IHttpClientFactory _clientFactory; // 定義HttpClient工廠

        // 透過構造函數注入HttpClientFactory
        public CommandController(IHttpClientFactory clientFactory)
        {
            _clientFactory = clientFactory;
        }

        // 定義一個Post方法處理指令發送
        [HttpPost("sendCommand")]
        public async Task<IActionResult> SendCommand([FromBody] CommandDto command) // 從請求體中獲取指令數據
        {
            var client = _clientFactory.CreateClient("ArduinoClient"); // 創建HttpClient實例
            var raspberryPiUrl = "http://192.168.0.111:7024/arduino_command"; // 定義樹莓派的地址

            try
            {
                var response = await client.PostAsJsonAsync(raspberryPiUrl, command);
                if (response.IsSuccessStatusCode)
                {
                    return Ok("Command sent to Raspberry Pi");
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    return StatusCode((int)response.StatusCode, $"Failed to send command: {errorContent}");
                }
            }
            catch (HttpRequestException e)
            {
                return StatusCode(500, $"Error sending command to Raspberry Pi: {e.Message}");
            }
        }
    }

    // 定義一個模型類，用於接收前端傳來的指令數據
    public class CommandDto
    {
        public string Command { get; set; } // 指令內容
    }
}
