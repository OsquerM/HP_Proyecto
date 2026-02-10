from sqlalchemy import Column, Integer, String
from backend.conexion import Base

class Casa(Base):
    __tablename__ = "casas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), unique=True, nullable=False)
    imagen = Column(String(255), nullable=False)  # URL o ruta de imagen
