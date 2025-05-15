import os
from cryptography.fernet import Fernet

folder = "C:\\Users\\jorda\\OneDrive\\Documents\\cible"


def load_key():
    return open("encrypte.key", "rb").read()

def decrypt_file(file, key):
    with open(file, "rb") as f:
        data = f.read()
    
    fernet = Fernet(key)
    decrypt_data = fernet.decrypt(data)
    
    with open(file.replace(".enc", ""), "wb") as f:
        f.write(decrypt_data)
    os.remove(file)
        
    print(f"File decrypted: {file}")
    
def decrypt_all_files(directory, key):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".enc"):
                decrypt_file(file_path, key)
                print(f"Decrypted {file_path}")

if __name__ == "__main__":
    key = load_key()
    decrypt_all_files(folder, key)