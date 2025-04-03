import sys
import os

def lire_fichier(file_path):
    """Lit un fichier et renvoie un set contenant ses lignes pour éviter les doublons."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(file.readlines())

def trouver_diff(file1_path, file2_path):
    """Compare deux fichiers et retourne les lignes présentes dans file2 mais absentes de file1."""
    file1_lines = lire_fichier(file1_path)
    file2_lines = lire_fichier(file2_path)

    return file2_lines - file1_lines  # Différence entre les deux fichiers

def enregistrer_diff(diff, output_file):
    """Enregistre les différences dans un fichier."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(diff)

def supprimer_fichiers(*fichiers):
    """Supprime les fichiers spécifiés."""
    for fichier in fichiers:
        try:
            os.remove(fichier)
            print(f"{fichier} supprimé avec succès.")
        except FileNotFoundError:
            print(f"{fichier} non trouvé.")
        except Exception as e:
            print(f"Erreur lors de la suppression de {fichier}: {e}")

if __name__ == "__main__":
    # Vérifie qu'on a bien les arguments nécessaires
    if len(sys.argv) != 4:
        print("Utilisation : python comparaison.py <fichier1> <fichier2> <fichier_sortie>")
        sys.exit(1)

    # Récupérer les fichiers depuis les arguments passés par Flask
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_file = sys.argv[3]

    # Effectuer la comparaison
    diff = trouver_diff(file1_path, file2_path)

    # Enregistrer les résultats
    enregistrer_diff(diff, output_file)

    # Supprimer les fichiers d'entrée
    supprimer_fichiers(file1_path, file2_path)

    print(f"Comparaison terminée. Différences enregistrées dans : {output_file}")
