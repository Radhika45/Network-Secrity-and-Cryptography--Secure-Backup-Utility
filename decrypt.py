# decrypt.py

import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEYS_DIR = "keys"
ENCRYPTED_DIR = "encrypted_files"
INPUT_ENC_FILE = "demo_file.txt.enc"

def load_private_key():
    with open(os.path.join(KEYS_DIR, "private_key.pem"), "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def rsa_decrypt_key(encrypted_key, private_key):
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def aes_decrypt_file(enc_file_path, aes_key):
    with open(enc_file_path, "rb") as f:
        content = f.read()

    iv = content[:16]
    ciphertext = content[16:]

    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    dec_file_path = enc_file_path.replace(".enc", ".dec")
    with open(dec_file_path, "wb") as f:
        f.write(decrypted_data)
    return dec_file_path

def main():
    print("Loading RSA private key...")
    private_key = load_private_key()

    encrypted_key_path = os.path.join(ENCRYPTED_DIR, "aes_key.encrypted")
    with open(encrypted_key_path, "rb") as f:
        encrypted_aes_key = f.read()

    print("Decrypting AES key with RSA private key...")
    aes_key = rsa_decrypt_key(encrypted_aes_key, private_key)

    enc_file_path = os.path.join(ENCRYPTED_DIR, INPUT_ENC_FILE)
    print(f"Decrypting file '{enc_file_path}' using AES key...")
    decrypted_file = aes_decrypt_file(enc_file_path, aes_key)

    print(f"Decryption complete! Recovered file saved as '{decrypted_file}'")

if __name__ == "__main__":
    main()
