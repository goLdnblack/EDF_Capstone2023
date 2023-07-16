import hashlib
import secrets

class HashGenerator():
    def __init__(self):
        return
    
    def generatePasswordSalt(self, password: str, salt):
        # Convert password string to byte type
        bytepass = bytes(password, 'utf-8')
        bytessalt = bytes(salt, 'utf-8')

        # Hash the password value with a salt to avoid
        # the same password having similar hash values
        hashed_password = hashlib.sha256(bytepass + 
                                         bytessalt).hexdigest()
        
        return hashed_password
    
    def generateSalt(self):
        # Generate a salt value to have
        # two different hash values for
        # two similar passwords
        salt = secrets.token_hex(8)
        return salt