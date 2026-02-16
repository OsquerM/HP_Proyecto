from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from . import models
from .database import get_db

quiz_router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Para servir HTML

# 🔹 Modelo Pydantic para recibir JSON del quiz
class RespuestaUsuario(BaseModel):
    usuario_nombre: str
    respuestas_usuario: dict  # {pregunta_id: respuesta_id}

# ============================
# Endpoint para obtener preguntas
# ============================
@quiz_router.get("/preguntas")
def obtener_preguntas(db: Session = Depends(get_db)):
    preguntas = db.query(models.Pregunta).all()
    resultado = []
    for pregunta in preguntas:
        respuestas = [
            {
                "id": r.id,
                "texto": r.texto_respuesta,
                "imagen": r.imagen  # ← agregar la imagen de cada respuesta
            }
            for r in pregunta.respuestas
        ]
        resultado.append({
            "id": pregunta.id,
            "texto_pregunta": pregunta.texto_pregunta,
            "respuestas": respuestas
        })
    return {"preguntas": resultado}

# ============================
# Endpoint para enviar respuestas y calcular casa
# ============================
@quiz_router.post("/enviar_respuestas")
def enviar_respuestas(
    datos: RespuestaUsuario,
    db: Session = Depends(get_db)
):
    usuario_nombre = datos.usuario_nombre
    respuestas_usuario = datos.respuestas_usuario

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

    # Guardar usuario y resultado en DB
    nuevo_usuario = models.Usuario(
        nombre=usuario_nombre,
        casa=casa_resultado
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"usuario": usuario_nombre, "casa": casa_resultado}

# ============================
# Nuevo endpoint: mostrar resultado en HTML
# ============================
@quiz_router.get("/resultado")
def mostrar_resultado(request: Request, nombre: str, casa: str):
    """
    Muestra el resultado del quiz con el nombre del usuario y la imagen de la casa
    """
    # Validar casa
    casas_validas = ["Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff"]
    if casa not in casas_validas:
        casa = "Gryffindor"
    
    # Nombre de la imagen según casa
    imagen_casa = f"uploads/{casa.lower()}.jpg"
    
    return templates.TemplateResponse(
        "resultado.html",
        {"request": request, "nombre": nombre, "casa": casa, "imagen_casa": imagen_casa}
    )
