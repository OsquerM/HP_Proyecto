from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuración de la base de datos
DB_USER = "root"
DB_PASSWORD = ""  # XAMPP por defecto no tiene contraseña para root
DB_HOST = "127.0.0.1"
DB_NAME = "harrypotter_quiz"

# URL de conexión
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Motor
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()