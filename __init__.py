from flask import Flask, render_template, request, redirect, jsonify, json
import sqlite3
from urllib.request import urlopen

def get_db_connection():
    conn = sqlite3.connect('/home/moulin2/www/flask/database.db')  # Remplacez 'database.db' par le chemin de votre base de données SQLite.
    conn.row_factory = sqlite3.Row  # Accès aux colonnes par nom.
    return conn

app = Flask(__name__)  # Création de l'application Flask

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")

# Création d'une nouvelle route pour la lecture de la BDD
@app.route("/consultation/")
def ReadBDD():
    conn = get_db_connection()  # Utilisation de la fonction définie pour la connexion
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)
@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/fiche_clientn/<string:nom>')
def Readfichenom(nom):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE nom LIKE ?', (nom,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/search_client', methods=['GET', 'POST'])
def Searchfiche():

    # nom = input("Nom client a chercher: ");
    if request.method == 'POST':
        nom = request.form['nom']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM livres WHERE nom = ?', (nom,))
        data = cursor.fetchall()
        conn.close()
        if data:
            return render_template('read_data.html', data=data)
        else:
            return "No client found with that name."
    else:     
       return "Method not allowed for..."

@app.route('/ajouter_utilisateur/', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        message = request.form['message']  # Assurez-vous que le formulaire a un champ pour 'message'

        # Insérer les données dans la base de données
        conn = get_db_connection()
        cursor = conn.cursor()
        if conn is not None:
            try:
                cursor.execute('INSERT INTO utilisateurs (nom, prenom, message) VALUES (?, ?, ?)', 
                               (nom, prenom, message))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Erreur de base de données: {e}")
                # Retourner une réponse ou rediriger avec un message d'erreur
            finally:
                conn.close()

        # Rediriger vers la page de consultation des utilisateurs après l'ajout
        return redirect('https://moulin2.alwaysdata.net/consultation/')  # Assurez-vous que ce chemin est correct

    # Si la méthode est GET, simplement rendre le template du formulaire
    return render_template('create_user.html')
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)
    def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL,
                        message TEXT)''')
    conn.commit()
    conn.close()

# Appelez init_db() quelque part avant de démarrer votre application, par exemple :
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
