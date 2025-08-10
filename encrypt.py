# encrypt.py

import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEYS_DIR = "keys"
ENCRYPTED_DIR = "encrypted_files"
INPUT_FILE = "demo_file.txt"

def generate_rsa_keys():
    print("Generating RSA key pair...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Save private key
    with open(os.path.join(KEYS_DIR, "private_key.pem"), "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Save public key
    public_key = private_key.public_key()
    with open(os.path.join(KEYS_DIR, "public_key.pem"), "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

def load_public_key():
    with open(os.path.join(KEYS_DIR, "public_key.pem"), "rb") as f:
        return serialization.load_pem_public_key(f.read())

def aes_encrypt_file(input_file_path):
    with open(input_file_path, "rb") as f:
        data = f.read()

    aes_key = os.urandom(32)  # AES-256 key
    iv = os.urandom(16)       # AES block size IV

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # Save encrypted file (IV + ciphertext)
    with open(os.path.join(ENCRYPTED_DIR, os.path.basename(input_file_path) + ".enc"), "wb") as f:
        f.write(iv + encrypted_data)

    return aes_key

def rsa_encrypt_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(os.path.join(ENCRYPTED_DIR, "aes_key.encrypted"), "wb") as f:
        f.write(encrypted_key)

def main():
    # Create directories if not exist
    os.makedirs(KEYS_DIR, exist_ok=True)
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)

    #Uncomment this to generate keys once, then comment it out
    #generate_rsa_keys()

    print("Loading public key...")
    public_key = load_public_key()

    print(f"Encrypting file '{INPUT_FILE}' with AES...")
    aes_key = aes_encrypt_file(INPUT_FILE)

    print("Encrypting AES key with RSA public key...")
    rsa_encrypt_key(aes_key, public_key)

    print("Encryption complete!")
    print(f"Encrypted file saved to '{ENCRYPTED_DIR}/{INPUT_FILE}.enc'")
    print(f"Encrypted AES key saved to '{ENCRYPTED_DIR}/aes_key.encrypted'")

if __name__ == "__main__":
    main()
