from flask import Flask, render_template, request, redirect, session
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('/home/moulin2/www/flask/database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

# Autres routes...

@app.route('/ajouter_utilisateur/', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        message = request.form['message']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO utilisateurs (nom, prenom, message) VALUES (?, ?, ?)', 
                           (nom, prenom, message))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur de base de données: {e}")
            # Retourner une réponse ou rediriger avec un message d'erreur
        finally:
            conn.close()

        return redirect('/consultation/')

    return render_template('create_user.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect('/')
        else:
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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

