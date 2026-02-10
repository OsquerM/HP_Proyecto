from sqlalchemy import Column, Integer, String
from backend.conexion import Base

class Pregunta(Base):
    __tablename__ = "preguntas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(255), nullable=False)
