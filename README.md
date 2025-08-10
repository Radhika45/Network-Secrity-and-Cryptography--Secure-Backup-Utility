## Setup Instructions

Step1:- Create a Python virtual environment and activate it.
Step2:- Install dependencies: `pip install -r requirements.txt`
Step3:- Create your own `demo_file.txt` with any content.
Step4:- Run `encrypt.py` to encrypt the file and AES key.
Step5:- Run `decrypt.py` to decrypt and recover the original file.

# Step 1: Generate RSA keys
python keys/keygen.py

# Step 2: Encrypt the file
python encrypt.py

# Step 3: Decrypt the file
python decrypt.py

### Git 
1. git init
2. git add .
3. git commit -m "Security"
4. git remote add origin https://github.com/Radhika45/NSC--Secure-Backup-Utility.git
5. git branch -M main
6. git push -u origin main
