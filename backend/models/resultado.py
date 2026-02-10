from sqlalchemy import Column, Integer, ForeignKey
from backend.conexion import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    casa_id = Column(Integer, ForeignKey("casas.id"), nullable=False)
