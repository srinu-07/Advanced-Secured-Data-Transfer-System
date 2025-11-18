from cryptography.fernet import Fernet
import os

def encrypt_file(filepath, key=None):
    if not key:
        key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(filepath, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data)
    encrypted_path = filepath + '.enc'

    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)

    return encrypted_path, key.decode()

def decrypt_file(filepath, key):
    fernet = Fernet(key.encode())

    with open(filepath, 'rb') as f:
        data = f.read()

    decrypted = fernet.decrypt(data)

    # Get original filename without .enc
    base = os.path.basename(filepath)
    if base.endswith('.enc'):
        original_name = base[:-4]  # remove '.enc'
    else:
        original_name = base + '.dec'

    decrypted_path = os.path.join('uploads/decrypted', original_name)

    with open(decrypted_path, 'wb') as f:
        f.write(decrypted)

    return decrypted_path
