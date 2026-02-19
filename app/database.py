from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 Configuración de conexión
# usuario: root
# contraseña: '' (vacío por defecto en XAMPP)
# host: localhost
# puerto: 3306 (default MySQL/MariaDB)
# base de datos: harryquiz
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/harryquiz"

# 🔹 Motor de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,   # evita errores de conexión muerta
    pool_recycle=3600,    # recicla conexiones cada 1 hora
    future=True           # compatibilidad moderna SQLAlchemy
)

# 🔹 Sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🔹 Base para modelos
Base = declarative_base()

# 🔹 Función para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
