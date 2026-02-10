from sqlalchemy import Column, Integer, String, ForeignKey
from backend.conexion import Base

class Respuesta(Base):
    __tablename__ = "respuestas"

    id = Column(Integer, primary_key=True, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"), nullable=False)
    texto = Column(String(255), nullable=False)
    casa_id = Column(Integer, ForeignKey("casas.id"), nullable=False)
