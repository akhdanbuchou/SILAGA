import bcrypt

def encrypt(password):
    '''
    menerima raw password, mengembalikan brypted password
    '''
    hashed = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode('ASCII')
    return hashed

def check(password, hashed):
    '''
    check apakah password cocok dengan hashed 
    '''
    return bcrypt.checkpw(str.encode(password), str.encode(hashed))
