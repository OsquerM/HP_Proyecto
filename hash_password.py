from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "1234"  
hashed = pwd_context.hash(password)
print(hashed)
