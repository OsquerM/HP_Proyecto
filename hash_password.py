from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "1234"  # aquí pones la contraseña que quieras
hashed = pwd_context.hash(password)
print(hashed)
