// joystick.js
document.addEventListener('CameraReady', function () {
    setupJoystick();
});

function setupJoystick() {
    var joystick = nipplejs.create({
        zone: document.getElementById('joystick-container'),
        mode: 'dynamic',
        color: 'blue',
    });

    joystick.on('move', function (evt, data) {
        if (data.direction) {
            switch (data.direction.angle) {
                case 'up': moveCar('W'); break;
                case 'down': moveCar('S'); break;
                case 'left': moveCar('A'); break;
                case 'right': moveCar('D'); break;
            }
        }
    });

    joystick.on('end', function () {
        moveCar('X');
    });
}

function moveCar(command) {
    fetch('/api/Command/sendCommand', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ Command: command }),
    })
    .then(response => {
        if (response.ok) {
            console.log(command);
        } else {
            console.error('Move Failure:', response.statusText);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
