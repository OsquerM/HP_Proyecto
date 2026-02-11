from fastapi import APIRouter, Form, UploadFile, File, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models
from .database import get_db
import shutil
import os

admin_router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==========================
# Mostrar panel de admin
# ==========================
@admin_router.get("/admin")
def mostrar_admin(request: Request, db: Session = Depends(get_db)):
    preguntas = db.query(models.Pregunta).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "preguntas": preguntas
        }
    )

# ==========================
# Agregar nueva pregunta con 4 respuestas e imágenes
# ==========================
@admin_router.post("/admin/agregar_pregunta")
def agregar_pregunta(
    texto_pregunta: str = Form(...),

    respuesta1: str = Form(...),
    casa1: str = Form(...),
    imagen1: UploadFile = File(...),

    respuesta2: str = Form(...),
    casa2: str = Form(...),
    imagen2: UploadFile = File(...),

    respuesta3: str = Form(...),
    casa3: str = Form(...),
    imagen3: UploadFile = File(...),

    respuesta4: str = Form(...),
    casa4: str = Form(...),
    imagen4: UploadFile = File(...),

    db: Session = Depends(get_db)
):
    # 🔹 Crear la pregunta (SIN imagen)
    pregunta = models.Pregunta(texto_pregunta=texto_pregunta)
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)

    # 🔹 Lista de respuestas
    respuestas_info = [
        (respuesta1, casa1, imagen1),
        (respuesta2, casa2, imagen2),
        (respuesta3, casa3, imagen3),
        (respuesta4, casa4, imagen4),
    ]

    for texto_respuesta, casa, archivo_imagen in respuestas_info:

        # Guardar imagen en static/uploads
        nombre_archivo = archivo_imagen.filename
        ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)

        with open(ruta_guardado, "wb") as buffer:
            shutil.copyfileobj(archivo_imagen.file, buffer)

        # Ruta que se guardará en la base de datos
        ruta_bd = f"uploads/{nombre_archivo}"

        respuesta = models.Respuesta(
            texto_respuesta=texto_respuesta,
            casa=casa,
            imagen=ruta_bd,
            pregunta_id=pregunta.id
        )

        db.add(respuesta)

    db.commit()

    return RedirectResponse(url="/admin", status_code=303)


# ==========================
# Eliminar pregunta
# ==========================
@admin_router.post("/admin/eliminar_pregunta")
def eliminar_pregunta(
    pregunta_id: int = Form(...),
    db: Session = Depends(get_db)
):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()

    if pregunta:
        db.delete(pregunta)
        db.commit()

    return RedirectResponse(url="/admin", status_code=303)


# ==========================
# Eliminar respuesta
# ==========================
@admin_router.post("/admin/eliminar_respuesta")
def eliminar_respuesta(
    respuesta_id: int = Form(...),
    db: Session = Depends(get_db)
):
    respuesta = db.query(models.Respuesta).filter_by(id=respuesta_id).first()

    if respuesta:
        db.delete(respuesta)
        db.commit()

    return RedirectResponse(url="/admin", status_code=303)
