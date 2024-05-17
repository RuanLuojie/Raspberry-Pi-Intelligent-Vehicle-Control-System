

fetch('json/test.json')
    .then(response => response.json()) 
    .then(data => {
        data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        const dialogueBox = document.getElementById('dialogue-box'); 

        data.forEach(dialogue => {
            const p = document.createElement('p');
            p.classList.add(dialogue.role);
            p.textContent = `${dialogue.role === 'assistant' ? '助手: ' : '用户: '}${dialogue.content}`;
            dialogueBox.appendChild(p);
        });
    })
.catch(error => console.error('Error loading dialogues:', error));

function showPopup(src) {
    document.getElementById('popup-img').src = src; // 设置弹出图片的源
    document.getElementById('popup').style.display = 'flex'; // 显示弹出层
}

// 隐藏图片弹出层
function hidePopup() {
    document.getElementById('popup').style.display = 'none'; // 隐藏弹出层
}

document.querySelectorAll('.image').forEach(img => {
    img.onmousedown = (e) => e.preventDefault(); // 防止鼠标按下时的选择
    img.onclick = () => showPopup(img.src);
});

