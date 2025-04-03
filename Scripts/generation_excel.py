import sys
import pandas as pd

# Définir les en-têtes du fichier
headers = [
    "Type d'identifiant PP", "Identifiant PP", "Identification nationale PP", 
    "Code civilité d'exercice", "Libellé civilité d'exercice", "Code civilité", 
    "Libellé civilité", "Nom d'exercice", "Prénom d'exercice", "Code profession", 
    "Libellé profession", "Code catégorie professionnelle", "Libellé catégorie professionnelle", 
    "Code type savoir-faire", "Libellé type savoir-faire", "Code savoir-faire", 
    "Libellé savoir-faire", "Code mode exercice", "Libellé mode exercice", 
    "Numéro SIRET site", "Numéro SIREN site", "Numéro FINESS site", 
    "Numéro FINESS établissement juridique", "Identifiant technique de la structure", 
    "Raison sociale site", "Enseigne commerciale site", 
    "Complément destinataire (coord. structure)", "Complément point géographique (coord. structure)", 
    "Numéro Voie (coord. structure)", "Indice répétition voie (coord. structure)", 
    "Code type de voie (coord. structure)", "Libellé type de voie (coord. structure)", 
    "Libellé Voie (coord. structure)", "Mention distribution (coord. structure)", 
    "Bureau cedex (coord. structure)", "Code postal (coord. structure)", 
    "Code commune (coord. structure)", "Libellé commune (coord. structure)", 
    "Code pays (coord. structure)", "Libellé pays (coord. structure)", 
    "Téléphone (coord. structure)", "Téléphone 2 (coord. structure)", 
    "Télécopie (coord. structure)", "Adresse e-mail (coord. structure)", 
    "Code Département (structure)", "Libellé Département (structure)", 
    "Ancien identifiant de la structure", "Autorité d'enregistrement", 
    "Code secteur d'activité", "Libellé secteur d'activité", 
    "Code section tableau pharmaciens", "Libellé section tableau pharmaciens", 
    "Code rôle", "Libellé rôle", "Code genre activité", "Libellé genre activité","test"
]

# Définir les départements à filtrer
departements_vise = ['88', '57', '54','75005']  # Vosges (88), Moselle (57), Meurthe-et-Moselle (54)

def load_data(file_path):
    """Charge un fichier texte et filtre les données selon le département"""
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            values = line.strip().split('|')
            
            if len(values) == len(headers):  # Vérifier que le nombre de colonnes est correct
                record = dict(zip(headers, values))
                
                # Vérifier si le code postal commence par un département ciblé
                code_departement = record.get("Code postal (coord. structure)", "")
                if code_departement and any(code_departement.startswith(dept) for dept in departements_vise):
                    data.append(record)
            else:
                print(f"Erreur : Ligne mal formée - {line}")

    return data

if __name__ == "__main__":
    # Vérifie qu'on a bien les arguments nécessaires
    if len(sys.argv) != 3:
        print("Utilisation : python generation_excel.py <fichier_diff> <fichier_sortie>")
        sys.exit(1)

    # Récupérer les fichiers depuis les arguments passés par Flask
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Charger les données filtrées
    data = load_data(input_file)

    # Convertir en DataFrame et enregistrer en Excel
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

    print(f"Données enregistrées dans {output_file}")
