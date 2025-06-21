from flask import Flask 
from flask import render_template
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask import session, redirect, url_for
from flask import flash

import os

UPLOAD_FOLDER = 'static/uploads'



 # Use a more secure key in production



app = Flask(__name__)

app.secret_key = 'supersecretkey123' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    my_name = "Satish"
    age = 20
    skills = ["Python", "Flask", "HTML", "CSS"]
    location  = "India"
    return render_template('about.html', name=my_name, age=age, skills=skills, location=location)


@app.route('/form')
def form():
    return render_template('form.html')



import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            age INTEGER,
            password TEXT,
            location TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Call this function only once at the top of app.py
init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[4], password):
            session['username'] = user[1]
            session['email'] = user[2]
            
            flash('✅ Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('❌ Invalid email or password', 'error')
            return redirect('/login')

    # GET request: just show login form — NO FLASH HERE
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    flash('✅ You have been logged out.', 'success')
    return redirect('/login')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    email = request.form['email']
    raw_password = request.form['password']
    password = generate_password_hash(raw_password)
    location = request.form['location']
    age = request.form['age']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, age, password, location)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, email, age, password, location))
    conn.commit()
    conn.close()

    return render_template('submit.html', username=username, email=email, password='********', age=age, location=location)


@app.route('/users')
def users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return render_template('user.html', users=rows)


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))
    

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('❌ No file part', 'error')
        return redirect('/upload')

    file = request.files['file']

    if file.filename == '':
        flash('⚠️ No file selected', 'error')
        return redirect('/upload')

    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    flash('✅ File uploaded successfully!', 'success')
    return redirect('/files')

@app.route('/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('files.html', files=files)






if __name__ == '__main__':
    app.run(debug=True)