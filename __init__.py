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

@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")

@app.route("/consultation/")
def ReadBDD():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM utilisateurs;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/fiche_clientn/<string:nom>')
def Readfichenom(nom):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE nom LIKE ?', (nom,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/search_client', methods=['GET', 'POST'])
def Searchfiche():
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
        nom = request.form['nom']
        prenom = request.form['prenom']
        message = request.form['message']
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

        return redirect('https://moulin2.alwaysdata.net/consultation/')

    return render_template('create_user.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
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

