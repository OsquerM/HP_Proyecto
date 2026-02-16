const canvas = document.getElementById("magicCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

class Particle {

    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;

        this.size = Math.random() * 3;
        this.speedY = Math.random() * 0.5 + 0.2;
        this.opacity = Math.random();
    }

    update() {
        this.y -= this.speedY;

        if (this.y < 0) {
            this.y = canvas.height;
            this.x = Math.random() * canvas.width;
        }
    }

    draw() {
        ctx.fillStyle = "rgba(255,215,0," + this.opacity + ")";
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function init() {

    for (let i = 0; i < 120; i++) {
        particles.push(new Particle());
    }

}

function animate() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(p => {
        p.update();
        p.draw();
    });

    requestAnimationFrame(animate);
}

init();
animate();
