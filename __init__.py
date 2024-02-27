from flask import Flask, render_template_string, render_template, jsonify
from flask import Flask, render_template, request, redirect
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/consultation/')
def consultation():
    conn = sqlite3.connect('/home/Rdtns/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    
    return render_template('read_data.html', data=data) 

if __name__ == "__main__":
    app.run(debug=True)
