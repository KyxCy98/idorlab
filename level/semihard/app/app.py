from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
import sqlite3
import base64
import os

app = Flask(__name__)
app.secret_key = 'supersecretkeyforlab'
DB_PATH = 'instance/app.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def encode_id(uid):
    return base64.urlsafe_b64encode(str(uid).encode()).decode().rstrip('=')

def decode_id(encoded):
    try:
        padding = 4 - (len(encoded) % 4)
        if padding != 4:
            encoded += '=' * padding
        decoded = base64.urlsafe_b64decode(encoded).decode()
        return int(decoded)
    except:
        return None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
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
            return redirect(url_for('dashboard'))
        else:
            return 'Login gagal!', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    docs = conn.execute('SELECT id, title, is_secret FROM documents WHERE owner_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('dashboard.html', documents=docs, encode_id=encode_id)

@app.route('/document/<encoded_id>')
def view_document(encoded_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    doc_id = decode_id(encoded_id)
    if doc_id is None:
        abort(404)
    
    conn = get_db()
    doc = conn.execute('SELECT * FROM documents WHERE id = ?', (doc_id,)).fetchone()
    conn.close()
    
    if not doc:
        abort(404)
    
    return render_template('document.html', document=doc)

@app.route('/debug/config')
def debug_config():
    conn = get_db()
    flag2 = conn.execute('SELECT value FROM config WHERE key = "flag2"').fetchone()
    conn.close()
    return jsonify({
        "debug": True,
        "environment": "development",
        "secret_flag": flag2['value'] if flag2 else "Not found",
        "database_path": DB_PATH
    })

@app.route('/api/users')
def list_users():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    conn = get_db()
    users = conn.execute('SELECT id, username, role FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
