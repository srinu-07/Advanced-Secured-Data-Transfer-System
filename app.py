from flask import Flask, request, send_file, render_template, jsonify
from utils.crypto_utils import encrypt_file, decrypt_file
from utils.ml_utils import get_strength_label, is_key_strong
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Folder setup
app.config['UPLOAD_FOLDER'] = 'uploads/encrypted'
app.config['DECRYPT_FOLDER'] = 'uploads/decrypted'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECRYPT_FOLDER'], exist_ok=True)

# Home page (Encryption UI)
@app.route('/')
def index():
    return render_template('index.html')

# Decryption page
@app.route('/decrypt')
def decrypt_page():
    return render_template('decrypt.html')

# Generate a new Fernet key and evaluate its strength
@app.route('/generate_key')
def generate_key():
    key = Fernet.generate_key().decode()
    strength = get_strength_label(key)
    return jsonify({'key': key, 'strength': strength})

# Encrypt uploaded file using provided key
@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    file = request.files.get('file')
    key = request.form.get('key')

    if not file or not key:
        return "Missing file or key", 400

    if not is_key_strong(key):
        return "Key is weak. Please generate a stronger key.", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        encrypted_path, _ = encrypt_file(filepath, key.encode())
        return send_file(encrypted_path, as_attachment=True)
    except Exception as e:
        return f"Encryption failed: {str(e)}", 500

# Decrypt uploaded encrypted file using provided key
@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    file = request.files.get('file')
    key = request.form.get('key')

    if not file or not key:
        return "Missing file or key", 400

    filepath = os.path.join(app.config['DECRYPT_FOLDER'], file.filename)
    file.save(filepath)

    try:
        decrypted_path = decrypt_file(filepath, key)
        return send_file(decrypted_path, as_attachment=True)
    except Exception as e:
        return f"Decryption failed: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)