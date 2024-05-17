document.addEventListener('DOMContentLoaded', function () {
    // 创建动态操纵杆
    var joystick = nipplejs.create({
        zone: document.getElementById('joystick-container'), // 容器元素
        mode: 'dynamic', // 动态模式
        color: 'blue', // 操纵杆颜色
    });

    let commandSent = false;

    joystick.on('move', function (evt, data) {
        if (data.direction && !commandSent) {
            switch (data.direction.angle) {
                case 'up':
                    sendCommand('W');
                    break;
                case 'down':
                    sendCommand('S');
                    break;
                case 'left':
                    sendCommand('A');
                    break;
                case 'right':
                    sendCommand('D');
                    break;
            }
            commandSent = true;
        }
    });

    joystick.on('end', function () {
        sendCommand('X');
        commandSent = false; // 重置状态
    });

    // 檢查攝影機畫面
    checkCameraConnection();
});

function sendCommand(command) {
    fetch('/api/Command/sendCommand', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ command: command })
    })
    .then(response => {
        if (response.ok) {
            console.log('Command sent:', command);
        } else {
            console.error('Command failed:', response.statusText);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function checkCameraConnection() {
    const video = document.getElementById('video');

    // 设置定时器每5秒检查一次
    setInterval(() => {
        const img = new Image();
        img.src = video.src;

        img.onload = function () {
            console.log("Camera connection is good."); // 摄像头画面可用
            restoreVideo();
        }

        img.onerror = function () {
            alert("伺服器已斷線，請確認伺服器正常運作"); // 显示提示信息
            replaceVideoWithSVG();
        }
    }, 5000); // 每5秒检查一次
}

function replaceVideoWithSVG(width, height) {
    const video = document.getElementById('video');
    if (video) {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("viewBox", "0 0 100 100");
        svg.setAttribute("width", width);
        svg.setAttribute("height", height);
        svg.innerHTML = `<circle cx="50" cy="50" r="20" fill="red" />`;
        svg.id = 'video'; // 保持相同的 ID 以便后续恢复
        video.parentNode.replaceChild(svg, video);
    }
}

function restoreVideo() {
    const svg = document.getElementById('video');
    if (svg && svg.nodeName === 'svg') {
        const img = document.createElement('img');
        img.src = 'http://192.168.0.111:8080/?action=stream';
        img.id = 'video';
        img.className = 'Camera';
        svg.parentNode.replaceChild(img, svg);
    }
}


