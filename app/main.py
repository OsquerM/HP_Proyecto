from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 🔹 Crear la app primero
app = FastAPI(title="Harry Potter Quiz")

# 🔹 Montar carpeta static para imágenes
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 Importar routers DESPUÉS de crear app
from .quiz import quiz_router
app.include_router(quiz_router)

# 🔹 Importar modelos y crear tablas
from .database import engine, Base
from . import models
Base.metadata.create_all(bind=engine)

# 🔹 Ruta inicial de prueba
@app.get("/")
def leer_inicio():
    return {"mensaje": "¡Hola! La base de datos y FastAPI están funcionando."}
