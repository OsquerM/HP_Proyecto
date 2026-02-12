from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db: Session = next(get_db())

# Verificar si ya existe
admin_existente = db.query(Usuario).filter_by(nombre="admin", rol="admin").first()

if admin_existente is None:
    admin = Usuario(
        nombre="admin",
        password=pwd_context.hash("1234"),  # contraseña hasheada
        rol="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("Admin creado:", admin.nombre)
else:
    # Actualizamos la contraseña por si queremos resetearla
    admin_existente.password = pwd_context.hash("1234")
    db.commit()
    print("Admin ya existía. Contraseña actualizada.")
