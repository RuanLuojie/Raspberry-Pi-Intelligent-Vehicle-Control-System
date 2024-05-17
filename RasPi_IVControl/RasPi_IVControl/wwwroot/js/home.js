document.addEventListener('DOMContentLoaded', function () {

    checkCameraConnection();
});


function checkCameraConnection() {
    const video = document.getElementById('video');

    setInterval(() => {
        const img = new Image();
        img.src = video.src;

        img.onload = function () {
            console.log("Camera connection is good."); // 摄像头画面可用
            restoreVideo(video.width, video.height);
        }

        img.onerror = function () {
            alert("伺服器已斷線，請確認伺服器正常運作"); // 显示提示信息
            replaceVideoWithSVG(video.width, video.height);
        }
    }, 5000);
}
function replaceVideoWithSVG(width, height) {
    const video = document.getElementById('video');
    if (video) {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("viewBox", "0 0 100 100");
        svg.setAttribute("width", width);
        svg.setAttribute("height", height);
        svg.innerHTML = `<circle cx="50" cy="50" r="20" fill="red" />`;
        svg.id = 'video'; 
        video.parentNode.replaceChild(svg, video);
    }
}

function restoreVideo(width, height) {
    const svg = document.getElementById('video');
    if (svg && svg.nodeName === 'svg') {
        const img = document.createElement('img');
        img.src = 'http://192.168.0.111:8080/?action=stream';
        img.id = 'video';
        img.className = 'Camera';
        img.setAttribute("width", width);
        img.setAttribute("height", height);
        svg.parentNode.replaceChild(img, svg);
    }
}