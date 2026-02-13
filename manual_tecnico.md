# Manual Técnico
## Proyecto: Sistema de Selección de Casas - Harry Potter
Autor: Óscar Manuel Benito Martín
Tecnologías: FastAPI, Jinja2, SQLAlchemy, SQLite, HTML, CSS

---

# 1. Descripción General

Este proyecto es una aplicación web desarrollada con FastAPI que permite:

- Mostrar preguntas tipo test.
- Asociar respuestas a casas de Hogwarts.
- Calcular la casa final según las respuestas.
- Administrar preguntas y respuestas desde un panel de administración.

---

# 2. Arquitectura del Proyecto

Estructura principal:

HP_Proyecto/
│
├── app/
│ ├── main.py
│ ├── admin.py
│ ├── models.py
│ ├── database.py
│ └── ...
│
├── templates/
│ ├── index.html
│ ├── resultado.html
│ ├── admin.html
│ ├── editar_pregunta.html
│ ├── editar_respuesta.html
│
├── static/
│ ├── css/
│ ├── imagenes/
│
└── requirements.txt

---

# 3. Tecnologías Utilizadas

- **FastAPI** → Framework backend
- **SQLAlchemy** → ORM para base de datos
- **SQLite** → Base de datos local
- **Jinja2** → Motor de plantillas
- **HTML/CSS** → Interfaz visual

---

# 4. Base de Datos

## 4.1 Modelo Pregunta

<!-- ```python
class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)

    respuestas = relationship("Respuesta", back_populates="pregunta", cascade="all, delete")
class Respuesta(Base):
    __tablename__ = "respuestas"

    id = Column(Integer, primary_key=True, index=True)
    texto_respuesta = Column(String, nullable=False)
    casa = Column(String, nullable=False)
    imagen = Column(String, nullable=True)

    pregunta_id = Column(Integer, ForeignKey("preguntas.id"))
    pregunta = relationship("Pregunta", back_populates="respuestas")
``` -->
# 5. Sistema de rutas
## 5.1 Rutas públicas
| Método | Ruta       | Función             |
| ------ | ---------- | ------------------- |
| GET    | /          | Mostrar test        |
| POST   | /resultado | Calcular casa final |
## 5.2 Rutas de administración
| Método | Ruta                         | Función                 |
| ------ | ---------------------------- | ----------------------- |
| GET    | /admin                       | Panel de administración |
| POST   | /admin/crear_pregunta        | Crear nueva pregunta    |
| POST   | /admin/eliminar_pregunta     | Eliminar pregunta       |
| GET    | /admin/editar_pregunta/{id}  | Formulario edición      |
| POST   | /admin/actualizar_pregunta   | Guardar cambios         |
| GET    | /admin/editar_respuesta/{id} | Editar respuesta        |
| POST   | /admin/actualizar_respuesta  | Guardar respuesta       |
# 6. Flujo de Funcionamiento
- El usuario responde preguntas.

- Se envían las respuestas al backend.

- Se cuentan las casas seleccionadas.

- Se determina la casa con mayor puntuación.

- Se muestra el resultado.

# 7. Gestión de imágenes
- Las imágenes se almacenan en /static/

- En la base de datos solo se guarda el nombre del archivo.

- Se accede desde el HTML con: 
```<img src="/static/{{ respuesta.imagen }}">```


# 8. Seguridad

- Actualmente el panel de administración no tiene autenticación.
Se recomienda implementar:

- Sistema de login

- Protección de rutas con dependencias

- Variables de entorno para producción

# 9. Ejecución del proyecto
## Instalación de dependencias 
 ```pip install -r requirements.txt ```
## Ejecución del servidor 
```uvicorn app.main:app --reload```
## Acceso a la url
```http://127.0.0.1:8000```
