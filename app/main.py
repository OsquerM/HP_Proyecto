from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# 🔹 Crear la app
app = FastAPI(title="Harry Potter Quiz")

# 🔹 Carpeta static para imágenes, CSS y JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 Carpeta templates para HTML
templates = Jinja2Templates(directory="templates")  # templates/ en la raíz

# 🔹 Importar routers
from .quiz import quiz_router
from .admin import admin_router  # si tienes admin

app.include_router(quiz_router)
app.include_router(admin_router)

# 🔹 Importar modelos y crear tablas
from .database import engine, Base
from . import models
Base.metadata.create_all(bind=engine)


# 🔹 Ruta inicial → index.html
@app.get("/", response_class=HTMLResponse)
def leer_inicio(request: Request):
    """
    Sirve el archivo index.html que está en templates/
    """
    return templates.TemplateResponse("index.html", {"request": request})


# 🔹 Ruta para mostrar index (opcional pero útil)
@app.get("/index", response_class=HTMLResponse)
def mostrar_index(request: Request):
    """
    Sirve el archivo index.html que está en templates/
    """
    return templates.TemplateResponse("index.html", {"request": request})


# 🔹 Ruta para mostrar quiz
@app.get("/quiz", response_class=HTMLResponse)
def mostrar_quiz(request: Request):
    """
    Sirve el archivo quiz.html que está en templates/
    """
    return templates.TemplateResponse("quiz.html", {"request": request})
