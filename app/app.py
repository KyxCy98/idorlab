from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DB_PATH = 'instance/app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile', user_id=session['user_id']))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('profile', user_id=user['id']))
        else:
            return 'Login gagal!', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        return 'User tidak ditemukan', 404
    
    return render_template('profile.html', user=user, current_user_id=session['user_id'])

@app.route('/backup')
def backup_db():
    if os.path.exists(DB_PATH):
        return send_file(DB_PATH, as_attachment=True, download_name='app_backup.db')
    else:
        return 'Database tidak ditemukan', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
