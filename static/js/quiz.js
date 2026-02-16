const BASE_URL = "http://127.0.0.1:8000"; 

async function cargarPreguntas() {

    const res = await fetch(`${BASE_URL}/preguntas`);
    const data = await res.json();

    const contenedor = document.getElementById("preguntas");

    data.preguntas.forEach(p => {

        const div = document.createElement("div");
        div.className = "pregunta";

        const titulo = document.createElement("p");
        titulo.textContent = p.texto_pregunta;
        div.appendChild(titulo);

        const grid = document.createElement("div");
        grid.className = "opciones-imagenes";

        p.respuestas.forEach(r => {

            const opcion = document.createElement("div");
            opcion.className = "opcion";

            opcion.innerHTML = `
                <img src="${BASE_URL}/static/${r.imagen}" alt="${r.texto}">
                <br>
                <input type="radio" name="pregunta_${p.id}" value="${r.id}" required>
                ${r.texto}
            `;

            grid.appendChild(opcion);

        });

        div.appendChild(grid);
        contenedor.appendChild(div);

    });

}

document.getElementById("quizForm").addEventListener("submit", async function(e) {

    e.preventDefault();

    const usuario = document.getElementById("usuario").value;

    const radios = document.querySelectorAll("input[type='radio']:checked");

    const respuestas_usuario = {};

    radios.forEach(r => {

        const pregunta_id = r.name.split("_")[1];
        respuestas_usuario[pregunta_id] = parseInt(r.value);

    });

    const res = await fetch(`${BASE_URL}/enviar_respuestas`, {

        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            usuario_nombre: usuario,
            respuestas_usuario
        })

    });

    const resultado = await res.json();

    // 🔹 REDIRECCIÓN A LA PÁGINA DE RESULTADO
    window.location.href =
        `${BASE_URL}/resultado?nombre=${resultado.usuario}&casa=${resultado.casa}`;

});

cargarPreguntas();
