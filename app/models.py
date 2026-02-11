from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# ========================
# Modelo Usuario
# ========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    password = Column(String(255), nullable=True)
    rol = Column(String(20), default="usuario")
    casa = Column(String(20), nullable=True)


# ========================
# Modelo Pregunta
# ========================
class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    texto_pregunta = Column(Text, nullable=False)

    # Relación con respuestas
    respuestas = relationship(
        "Respuesta",
        back_populates="pregunta",
        cascade="all, delete-orphan"
    )


# ========================
# Modelo Respuesta
# ========================
class Respuesta(Base):
    __tablename__ = "respuestas"

    id = Column(Integer, primary_key=True, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id", ondelete="CASCADE"), nullable=False)
    texto_respuesta = Column(String(255), nullable=False)
    casa = Column(String(20), nullable=False)  # Gryffindor, Slytherin, Ravenclaw, Hufflepuff
    imagen = Column(String(255), nullable=True)  # Para la imagen de la opción

    # Relación inversa con pregunta
    pregunta = relationship("Pregunta", back_populates="respuestas")
