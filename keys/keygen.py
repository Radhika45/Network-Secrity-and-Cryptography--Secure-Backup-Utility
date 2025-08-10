from Crypto.PublicKey import RSA

def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open('keys/private_key.pem', 'wb') as prv_file:
        prv_file.write(private_key)
    with open('keys/public_key.pem', 'wb') as pub_file:
        pub_file.write(public_key)

    print("RSA key pair generated and saved to keys folder.")

if __name__ == "__main__":
    generate_keys()
