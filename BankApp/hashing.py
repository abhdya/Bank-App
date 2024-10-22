from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class Hash():
    @staticmethod
    def hash_argon(password: str):
        hashed_password = pwd_context.hash(password)
        return hashed_password
    
    @staticmethod
    def verify(hashed_password, entered_password):
        return pwd_context.verify(entered_password, hashed_password)
