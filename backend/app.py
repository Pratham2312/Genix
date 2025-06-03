# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'

# # DB setup
# def init_db():
#     conn = sqlite3.connect('database.db')
#     conn.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             password TEXT NOT NULL,
#             role TEXT NOT NULL
#         )
#     ''')
#     conn.close()

# init_db()

# # Routes
# @app.route('/')
# def index():
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         role = request.form['role']
#         email = request.form['email']
#         password = request.form['password']

#         conn = sqlite3.connect('database.db')
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM users WHERE email=? AND role=?", (email, role))
#         user = cur.fetchone()
#         conn.close()

#         if user and check_password_hash(user[3], password):
#             session['user'] = user[1]
#             session['role'] = user[4]
#             flash("Login successful!", "success")
#             return f"Welcome {user[1]}! You are logged in as a {user[4]}."
#         else:
#             flash("Invalid credentials", "danger")

#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
#         role = request.form['role']

#         try:
#             conn = sqlite3.connect('database.db')
#             cur = conn.cursor()
#             cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
#                         (name, email, password, role))
#             conn.commit()
#             conn.close()
#             flash("Signup successful! Please log in.", "success")
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             flash("Email already registered!", "warning")

#     return render_template('signup.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("You have been logged out.", "info")
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# DB setup
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND role=?", (email, role))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]
            session['role'] = user[4]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                        (name, email, password, role))
            conn.commit()
            conn.close()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already registered!", "warning")

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', name=session['user'], role=session['role'])
    else:
        flash("Login required", "warning")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)
