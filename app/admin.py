from fastapi import APIRouter, Form, UploadFile, File, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models
from .database import get_db
import shutil
import os
import uuid

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
        {"request": request, "preguntas": preguntas}
    )


# ==========================
# Agregar nueva pregunta
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
    # Crear pregunta
    pregunta = models.Pregunta(texto_pregunta=texto_pregunta)
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)

    respuestas_info = [
        (respuesta1, casa1, imagen1),
        (respuesta2, casa2, imagen2),
        (respuesta3, casa3, imagen3),
        (respuesta4, casa4, imagen4),
    ]

    for texto_respuesta, casa, archivo_imagen in respuestas_info:

        # Nombre único para evitar sobreescritura
        nombre_archivo = f"{uuid.uuid4()}_{archivo_imagen.filename}"
        ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)

        with open(ruta_guardado, "wb") as buffer:
            shutil.copyfileobj(archivo_imagen.file, buffer)

        ruta_bd = f"uploads/{nombre_archivo}"

        respuesta = models.Respuesta(
            texto_respuesta=texto_respuesta,
            casa=casa,
            imagen=ruta_bd,
            pregunta_id=pregunta.id
        )

        db.add(respuesta)

    db.commit()

    return RedirectResponse("/admin", status_code=303)


# ==========================
# Eliminar pregunta
# ==========================
@admin_router.post("/admin/eliminar_pregunta")
def eliminar_pregunta(
    pregunta_id: int = Form(...),
    db: Session = Depends(get_db)
):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()

    if not pregunta:
        return RedirectResponse("/admin", status_code=303)

    db.delete(pregunta)
    db.commit()

    return RedirectResponse("/admin", status_code=303)


# ==========================
# Eliminar respuesta
# ==========================
@admin_router.post("/admin/eliminar_respuesta")
def eliminar_respuesta(
    respuesta_id: int = Form(...),
    db: Session = Depends(get_db)
):
    respuesta = db.query(models.Respuesta).filter_by(id=respuesta_id).first()

    if not respuesta:
        return RedirectResponse("/admin", status_code=303)

    db.delete(respuesta)
    db.commit()

    return RedirectResponse("/admin", status_code=303)


# ==========================
# Mostrar formulario editar pregunta
# ==========================
@admin_router.get("/admin/editar_pregunta/{pregunta_id}")
def editar_pregunta(
    pregunta_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()

    if not pregunta:
        return RedirectResponse("/admin", status_code=303)

    return templates.TemplateResponse(
        "editar_pregunta.html",
        {"request": request, "pregunta": pregunta}
    )


# ==========================
# Actualizar pregunta
# ==========================
@admin_router.post("/admin/actualizar_pregunta")
def actualizar_pregunta(
    pregunta_id: int = Form(...),
    texto_pregunta: str = Form(...),
    db: Session = Depends(get_db)
):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()

    if pregunta:
        pregunta.texto_pregunta = texto_pregunta
        db.commit()

    return RedirectResponse("/admin", status_code=303)


# ==========================
# Actualizar respuesta
# ==========================
@admin_router.post("/admin/actualizar_respuesta")
def actualizar_respuesta(
    respuesta_id: int = Form(...),
    texto_respuesta: str = Form(...),
    casa: str = Form(...),
    imagen: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    respuesta = db.query(models.Respuesta).filter_by(id=respuesta_id).first()

    if not respuesta:
        return RedirectResponse("/admin", status_code=303)

    respuesta.texto_respuesta = texto_respuesta
    respuesta.casa = casa

    # Si suben nueva imagen
    if imagen and imagen.filename:
        nombre_archivo = f"{uuid.uuid4()}_{imagen.filename}"
        ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)

        with open(ruta_guardado, "wb") as buffer:
            shutil.copyfileobj(imagen.file, buffer)

        respuesta.imagen = f"uploads/{nombre_archivo}"

    db.commit()

    return RedirectResponse("/admin", status_code=303)
