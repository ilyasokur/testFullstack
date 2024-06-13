from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'test'


# Форма авторизации
@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    login = request.form['login']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    user = cursor.fetchone()

    if user:
        session['user'] = user[1]
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE responsible_full_name = ?", (user,))
    clients = cursor.fetchall()

    return render_template('dashboard.html', clients=clients, user=user)


@app.route('/update_status', methods=['POST'])
def update_status():
    if 'user' not in session:
        return redirect(url_for('login'))

    client_id = request.form['client_id']
    new_status = request.form['status']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE clients SET status = ? WHERE id = ?", (new_status, client_id))
    conn.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
