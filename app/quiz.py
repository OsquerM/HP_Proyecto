from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import models
from .database import get_db

quiz_router = APIRouter()

# ============================
# Endpoint para obtener preguntas
# ============================
@quiz_router.get("/preguntas")
def obtener_preguntas(db: Session = Depends(get_db)):
    preguntas = db.query(models.Pregunta).all()
    resultado = []
    for pregunta in preguntas:
        respuestas = [{"id": r.id, "texto": r.texto_respuesta} for r in pregunta.respuestas]
        resultado.append({
            "id": pregunta.id,
            "texto_pregunta": pregunta.texto_pregunta,
            "imagen": pregunta.imagen,
            "respuestas": respuestas
        })
    return {"preguntas": resultado}

# ============================
# Endpoint para enviar respuestas y calcular casa
# ============================
@quiz_router.post("/enviar_respuestas")
def enviar_respuestas(
    usuario_nombre: str,
    respuestas_usuario: dict,  # formato: {pregunta_id: respuesta_id}
    db: Session = Depends(get_db)
):
    # Contador de casas
    contador_casas = {
        "Gryffindor": 0,
        "Slytherin": 0,
        "Ravenclaw": 0,
        "Hufflepuff": 0
    }

    # Calcular puntos por casa
    for pregunta_id, respuesta_id in respuestas_usuario.items():
        respuesta = db.query(models.Respuesta).filter_by(id=respuesta_id).first()
        if respuesta:
            contador_casas[respuesta.casa] += 1

    # Elegir casa con más puntos
    casa_resultado = max(contador_casas, key=contador_casas.get)

    # Guardar usuario y resultado en la base de datos
    nuevo_usuario = models.Usuario(
        nombre=usuario_nombre,
        casa=casa_resultado
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"usuario": usuario_nombre, "casa": casa_resultado}
