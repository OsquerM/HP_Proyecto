from fastapi import APIRouter, Form, UploadFile, File, Request, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
from .database import get_db
import shutil
import os
import uuid

admin_router = APIRouter()
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ========================
# Contexto de hashing de contraseñas
# ========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ========================
# Dependency: verificar login
# ========================
def get_current_admin(admin_logged_in: str | None = Cookie(None)):
    if admin_logged_in != "true":
        raise HTTPException(status_code=401, detail="No autorizado")

# ========================
# Mostrar formulario login
# ========================
@admin_router.get("/admin/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ========================
# Procesar login
# ========================
@admin_router.post("/admin/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = db.query(models.Usuario).filter_by(nombre=username, rol="admin").first()
    if not admin or not verify_password(password, admin.password):
        return RedirectResponse("/admin/login", status_code=303)

    response = RedirectResponse("/admin", status_code=303)
    response.set_cookie(key="admin_logged_in", value="true")
    return response

# ========================
# Mostrar panel admin (protegido)
# ========================
@admin_router.get("/admin")
def mostrar_admin(request: Request, db: Session = Depends(get_db), _ = Depends(get_current_admin)):
    preguntas = db.query(models.Pregunta).all()
    return templates.TemplateResponse("admin.html", {"request": request, "preguntas": preguntas})

# ========================
# Agregar nueva pregunta
# ========================
@admin_router.post("/admin/agregar_pregunta")
def agregar_pregunta(
    texto_pregunta: str = Form(...),
    respuesta1: str = Form(...), casa1: str = Form(...), imagen1: UploadFile = File(...),
    respuesta2: str = Form(...), casa2: str = Form(...), imagen2: UploadFile = File(...),
    respuesta3: str = Form(...), casa3: str = Form(...), imagen3: UploadFile = File(...),
    respuesta4: str = Form(...), casa4: str = Form(...), imagen4: UploadFile = File(...),
    db: Session = Depends(get_db),
    _ = Depends(get_current_admin)
):
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
        if texto_respuesta.strip() == "":
            continue

        ruta_bd = None
        if archivo_imagen and archivo_imagen.filename.strip():
            nombre_archivo = f"{uuid.uuid4().hex}_{archivo_imagen.filename}"
            ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)
            with archivo_imagen.file as buffer, open(ruta_guardado, "wb") as f:
                shutil.copyfileobj(buffer, f)
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

# ========================
# Eliminar pregunta
# ========================
@admin_router.post("/admin/eliminar_pregunta")
def eliminar_pregunta(pregunta_id: int = Form(...), db: Session = Depends(get_db), _ = Depends(get_current_admin)):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()
    if pregunta:
        for respuesta in pregunta.respuestas:
            if respuesta.imagen:
                ruta_archivo = os.path.join("static", respuesta.imagen)
                if os.path.exists(ruta_archivo):
                    os.remove(ruta_archivo)
        db.delete(pregunta)
        db.commit()
    return RedirectResponse("/admin", status_code=303)

# ========================
# Eliminar respuesta individual
# ========================
@admin_router.post("/admin/eliminar_respuesta")
def eliminar_respuesta(respuesta_id: int = Form(...), db: Session = Depends(get_db), _ = Depends(get_current_admin)):
    respuesta = db.query(models.Respuesta).filter_by(id=respuesta_id).first()
    if respuesta:
        if respuesta.imagen:
            ruta_archivo = os.path.join("static", respuesta.imagen)
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
        db.delete(respuesta)
        db.commit()
    return RedirectResponse("/admin", status_code=303)

# ========================
# Editar pregunta
# ========================
@admin_router.get("/admin/editar_pregunta/{pregunta_id}")
def editar_pregunta(pregunta_id: int, request: Request, db: Session = Depends(get_db), _ = Depends(get_current_admin)):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()
    if not pregunta:
        return RedirectResponse("/admin", status_code=303)
    return templates.TemplateResponse("editar_pregunta.html", {"request": request, "pregunta": pregunta})

# ========================
# Actualizar pregunta y sus respuestas
# ========================
@admin_router.post("/admin/actualizar_pregunta")
def actualizar_pregunta(
    pregunta_id: int = Form(...),
    texto_pregunta: str = Form(...),
    respuesta1: str = Form(...), casa1: str = Form(...), imagen1: UploadFile | None = File(None),
    respuesta2: str = Form(...), casa2: str = Form(...), imagen2: UploadFile | None = File(None),
    respuesta3: str = Form(...), casa3: str = Form(...), imagen3: UploadFile | None = File(None),
    respuesta4: str = Form(...), casa4: str = Form(...), imagen4: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    _ = Depends(get_current_admin)
):
    pregunta = db.query(models.Pregunta).filter_by(id=pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    # Actualizar texto de la pregunta
    pregunta.texto_pregunta = texto_pregunta

    respuestas_info = [
        (respuesta1, casa1, imagen1),
        (respuesta2, casa2, imagen2),
        (respuesta3, casa3, imagen3),
        (respuesta4, casa4, imagen4),
    ]

    for idx, (texto, casa, archivo_imagen) in enumerate(respuestas_info):
        if idx < len(pregunta.respuestas):
            r = pregunta.respuestas[idx]
            r.texto_respuesta = texto
            r.casa = casa

            if archivo_imagen and archivo_imagen.filename.strip():
                # Borrar imagen antigua si existe
                if r.imagen:
                    ruta_antigua = os.path.join("static", r.imagen)
                    if os.path.exists(ruta_antigua):
                        os.remove(ruta_antigua)

                # Guardar nueva imagen
                nombre_archivo = f"{uuid.uuid4().hex}_{archivo_imagen.filename}"
                ruta_guardado = os.path.join(UPLOAD_DIR, nombre_archivo)
                with archivo_imagen.file as buffer, open(ruta_guardado, "wb") as f:
                    shutil.copyfileobj(buffer, f)
                r.imagen = f"uploads/{nombre_archivo}"

    db.commit()
    return RedirectResponse("/admin", status_code=303)

# ========================
# Logout del admin
# ========================
@admin_router.get("/admin/logout")
def logout(_ = Depends(get_current_admin)):
    response = RedirectResponse("/admin/login", status_code=303)
    response.delete_cookie("admin_logged_in")
    return response
