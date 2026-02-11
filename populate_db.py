from app import models
from app.database import SessionLocal, engine

# 🔹 Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

# 🔹 Crear sesión
db = SessionLocal()

# ======================
# Lista de preguntas a agregar o actualizar
# ======================
quiz_preguntas = [
    {
        "texto": "¿Cuál es tu materia favorita?",
        "respuestas": [
            {"texto": "Defensa Contra las Artes Oscuras", "casa": "Gryffindor", "imagen": "uploads/materia1.jpg"},
            {"texto": "Pociones", "casa": "Slytherin", "imagen": "uploads/materia2.jpg"},
            {"texto": "Runas Antiguas", "casa": "Ravenclaw", "imagen": "uploads/materia3.jpg"},
            {"texto": "Cuidado de Criaturas Mágicas", "casa": "Hufflepuff", "imagen": "uploads/materia4.jpg"},
        ]
    },
    {
        "texto": "¿Cuál es tu hechizo favorito?",
        "respuestas": [
            {"texto": "Expecto Patronum", "casa": "Gryffindor", "imagen": "uploads/patronus1.jpg"},
            {"texto": "Expelliarmus", "casa": "Slytherin", "imagen": "uploads/patronus2.jpg"},
            {"texto": "Lumos", "casa": "Ravenclaw", "imagen": "uploads/patronus3.jpg"},
            {"texto": "Alohomora", "casa": "Hufflepuff", "imagen": "uploads/patronus4.jpg"},
        ]
    }
]

# ======================
# Insertar o actualizar preguntas
# ======================
for pregunta in quiz_preguntas:
    texto_pregunta = pregunta["texto"]

    # Buscar si la pregunta ya existe
    pregunta_en_db = db.query(models.Pregunta).filter_by(texto_pregunta=texto_pregunta).first()

    if pregunta_en_db:
        print(f"La pregunta '{texto_pregunta}' ya existe. Se actualizarán sus respuestas e imágenes.")
    else:
        # Crear nueva pregunta
        pregunta_en_db = models.Pregunta(texto_pregunta=texto_pregunta)
        db.add(pregunta_en_db)
        db.commit()
        db.refresh(pregunta_en_db)
        print(f"Pregunta '{texto_pregunta}' agregada correctamente.")

    # ======================
    # Insertar o actualizar respuestas de esta pregunta
    # ======================
    for respuesta in pregunta["respuestas"]:
        texto_respuesta = respuesta["texto"]
        casa_respuesta = respuesta["casa"]
        imagen_respuesta = respuesta["imagen"]

        # Buscar si la respuesta ya existe
        respuesta_en_db = db.query(models.Respuesta).filter_by(
            pregunta_id=pregunta_en_db.id,
            texto_respuesta=texto_respuesta
        ).first()

        if respuesta_en_db:
            # Actualizar casa e imagen
            respuesta_en_db.casa = casa_respuesta
            respuesta_en_db.imagen = imagen_respuesta
            print(f"Respuesta '{texto_respuesta}' actualizada.")
        else:
            # Crear nueva respuesta
            nueva_respuesta = models.Respuesta(
                texto_respuesta=texto_respuesta,
                casa=casa_respuesta,
                imagen=imagen_respuesta,
                pregunta_id=pregunta_en_db.id
            )
            db.add(nueva_respuesta)
            print(f"Respuesta '{texto_respuesta}' agregada.")

    # Guardar cambios de respuestas
    db.commit()

# 🔹 Cerrar sesión
db.close()
print("Actualización de preguntas y respuestas completada.")
