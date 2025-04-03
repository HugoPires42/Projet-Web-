from flask import Flask, request, redirect, url_for, send_file, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'Uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    fichier_genere = False  # Par défaut, il n'y a pas de fichier généré

    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1 and file2:
            path1 = os.path.join(app.config['UPLOAD_FOLDER'], '1.txt')
            path2 = os.path.join(app.config['UPLOAD_FOLDER'], '2.txt')
            file1.save(path1)
            file2.save(path2)

            # Spécifiez le chemin de résultat pour le fichier 'result_diff.txt'
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_diff.txt')

            # Lancer le script de comparaison et générer 'result_diff.txt'
            subprocess.run(['python', 'Scripts/comparaison.py', path1, path2, result_path])

            # Vérifier si le fichier result_diff.txt a été généré
            if not os.path.exists(result_path):
                return "Erreur : Le fichier 'result_diff.txt' n'a pas été généré.", 500

            # Lancer le script de génération Excel
            output_excel = os.path.join(app.config['UPLOAD_FOLDER'], 'sortie.xlsx')
            subprocess.run(['python', 'Scripts/generation_excel.py', result_path, output_excel])

            # Vérifier si le fichier Excel a été généré
            if os.path.exists(output_excel):
                fichier_genere = True

    return render_template('index.html', fichier_genere=fichier_genere)

@app.route('/download')
def download_file():
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sortie.xlsx')
    if not os.path.exists(file_path):
        return "Erreur : Fichier de sortie non trouvé.", 500
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
