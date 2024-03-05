from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__) # création de l'application Flask

# Fonction pour établir la connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('/home/raid/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route pour afficher le formulaire
@app.route('/consultationn') 
def consultationn():
    return render_template("formulaire.html")

# Route pour lire les données depuis la base de données
@app.route("/consultation")
def ReadBDD():
    # Connexion à la base de données
    conn = sqlite3.connect('/home/raid/database.db')
    cursor = conn.cursor()
    
    # Exécution de la requête SQL pour sélectionner toutes les données de la table 'clients'
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    
    # Fermeture de la connexion à la base de données
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

# Route pour ajouter un message
@app.route('/messages', methods=['GET', 'POST'])
def ajouter_message():
    if request.method == 'POST':
        FatherName = request.form['fathername']
        MotherName = request.form['mothername']
        PermanentAddress = request.form['permanentaddress']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (fathername, mothername, permanentaddress) VALUES (?, ?, ?)', (FatherName, MotherName, PermanentAddress))
        conn.commit()
        
        conn.close() # Fermer la connexion à la base de données
        
        return redirect('/confirmation.html') # Rediriger vers la page de confirmation
        
    return render_template('message.html')

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template("index.html")

# Route pour le premier résumé
@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

# Route pour le deuxième résumé
@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

# Route pour le modèle de CV
@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")

# Exécution de l'application Flask
if __name__ == "__main__":
    app.run()
