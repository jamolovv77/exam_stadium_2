// ===== 1. Show the "players needed" input only when there is no team =====
document.addEventListener('change', function (e) {
    if (e.target.name !== 'has_team') return;

    var players = e.target.form.querySelector('.players');
    players.style.display = e.target.value === 'no' ? 'block' : 'none';
});


// ===== 2. Interactive football =====
(function () {
    var ball = document.getElementById('ball');
    if (!ball) return;

    var SIZE = 56;               // ball size in px
    var GRASS_GAP = 6;           // how high the ball stands above the screen bottom
    var GRAVITY = 0.55;          // pulls the ball down
    var AIR = 0.995;             // air resistance
    var FLOOR_FRICTION = 0.985;  // rolling friction on the grass
    var BOUNCE = 0.72;           // speed kept after a bounce
    var MAX_SPEED = 38;          // speed limit

    var x = 60;
    var y = 0;
    var vx = 0;
    var vy = 0;
    var angle = 0;
    var dragging = false;
    var lastX = null;
    var lastY = null;

    function limit(value) {
        return Math.max(-MAX_SPEED, Math.min(MAX_SPEED, value));
    }

    function getFloor() {
        return window.innerHeight - SIZE - GRASS_GAP;
    }

    // main loop: moves the ball about 60 times per second
    function step() {
        var floor = getFloor();
        var right = window.innerWidth - SIZE;

        if (!dragging) {
            vy += GRAVITY;
            vx *= AIR;
            x += vx;
            y += vy;

            // grass (floor)
            if (y >= floor) {
                y = floor;
                vy = Math.abs(vy) < 2 ? 0 : -vy * BOUNCE;
                vx *= FLOOR_FRICTION;
                if (Math.abs(vx) < 0.05) vx = 0;
            }
            // ceiling
            if (y <= 0) {
                y = 0;
                vy = Math.abs(vy) * BOUNCE;
            }
            // walls
            if (x <= 0) {
                x = 0;
                vx = Math.abs(vx) * BOUNCE;
            }
            if (x >= right) {
                x = right;
                vx = -Math.abs(vx) * BOUNCE;
            }

            // the ball spins while it moves
            angle += vx * 2.5;
        }

        ball.style.transform = 'translate(' + x + 'px, ' + y + 'px) rotate(' + angle + 'deg)';
        requestAnimationFrame(step);
    }

    // mouse kicks the ball (or drags it)
    document.addEventListener('pointermove', function (e) {
        var moveX = lastX === null ? 0 : e.clientX - lastX;
        var moveY = lastY === null ? 0 : e.clientY - lastY;
        lastX = e.clientX;
        lastY = e.clientY;

        if (dragging) {
            x = Math.min(Math.max(e.clientX - SIZE / 2, 0), window.innerWidth - SIZE);
            y = Math.min(Math.max(e.clientY - SIZE / 2, 0), getFloor());
            vx = limit(moveX);
            vy = limit(moveY);
            angle += moveX * 2.5;
            return;
        }

        var dx = (x + SIZE / 2) - e.clientX;
        var dy = (y + SIZE / 2) - e.clientY;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
        var speed = Math.sqrt(moveX * moveX + moveY * moveY);

        // the mouse touches the ball and moves fast enough
        if (dist < SIZE / 2 + 10 && speed > 2) {
            vx = limit((dx / dist) * (speed * 0.5 + 3) + moveX * 0.5);
            vy = limit((dy / dist) * (speed * 0.5 + 3) + moveY * 0.5 - 3);
            document.body.classList.add('kicked');
        }
    });

    // grab the ball and throw it
    ball.addEventListener('pointerdown', function (e) {
        dragging = true;
        ball.setPointerCapture(e.pointerId);
        document.body.classList.add('kicked');
        e.preventDefault();
    });

    ball.addEventListener('pointerup', function () {
        dragging = false;
    });

    ball.addEventListener('pointercancel', function () {
        dragging = false;
    });

    // the ball kicks itself every few seconds when it is resting
    setInterval(function () {
        var resting = !dragging && Math.abs(vx) < 0.5 && y >= getFloor() - 1;
        if (!resting) return;

        vx = (Math.random() < 0.5 ? -1 : 1) * (6 + Math.random() * 8);
        vy = -(9 + Math.random() * 7);
    }, 3500);

    // keep the ball inside the window after resize
    window.addEventListener('resize', function () {
        x = Math.min(x, window.innerWidth - SIZE);
        y = Math.min(y, getFloor());
    });

    step();
})();