 // 🔹 Música
    const music = document.getElementById("bgMusic");
    const btn = document.getElementById("musicButton");

    let playing = false;

    // Función para alternar música
    function toggleMusic() {
        if (music.paused) {
            music.play();
            btn.innerText = "🔊 Música ON";
            playing = true;
        } else {
            music.pause();
            btn.innerText = "🔇 Música OFF";
            playing = false;
        }
    }

    // Evento click en el botón
    btn.addEventListener("click", toggleMusic);

    // Activar música la primera vez que el usuario interactúa
    document.body.addEventListener("click", function initMusic() {
        if (!playing) {
            music.play().then(() => {
                btn.innerText = "🔊 Música ON";
                playing = true;
            }).catch(err => {
                console.log("Autoplay bloqueado, espera a pulsar el botón");
            });
        }
        // Solo necesitamos esto una vez
        document.body.removeEventListener("click", initMusic);
    });