from conexion import Base, engine
from models.usuario import Usuario
from models.casa import Casa
from models.pregunta import Pregunta
from models.respuesta import Respuesta
from models.resultado import Resultado

def init_db():
    Base.metadata.create_all(bind=engine)
    print("¡Tablas creadas correctamente!")

if __name__ == "__main__":
    init_db()
