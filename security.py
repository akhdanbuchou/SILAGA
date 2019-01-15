import bcrypt

def encrypt(password):
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode('ASCII')
    return hashed

def check(password, hashed):
    return bcrypt.checkpw(str.encode(password), str.encode(hashed))
