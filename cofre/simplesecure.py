import M2Crypto as m2c
from errors import Error
KEY = None

def load(key):
    global KEY
    try:
        KEY = m2c.RSA.load_key(key)
    except Exception, ex:
        raise Error('invalid password')
    
    
def encrypt(data):
    global KEY
    return KEY.public_encrypt(data, m2c.RSA.pkcs1_padding).encode('base64')


def decrypt(data):        
    global KEY
    return KEY.private_decrypt(data.decode('base64'), m2c.RSA.pkcs1_padding)
