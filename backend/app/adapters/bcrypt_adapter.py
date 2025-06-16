import bcrypt

class BcryptAdapter:
    
    @staticmethod
    def hash(value: str) -> str:
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def check(value: str, hashed_value: str) -> bool:
        return bcrypt.checkpw(value.encode('utf-8'), hashed_value.encode('utf-8'))    