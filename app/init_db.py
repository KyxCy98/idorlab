import sqlite3
import os

DB_PATH = 'instance/app.db'

def init_db():
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            fullname TEXT,
            flag TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY,
            secret_flag TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, password, role, fullname, flag)
        VALUES (1, 'admin', 'admin123', 'admin', 'Administrator', 'FLAG{1D0R_2_4dm1n_Pr0f1l3}')
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, password, role, fullname, flag)
        VALUES (2, 'user', 'user123', 'user', 'Budi Santoso', NULL)
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, password, role, fullname, flag)
        VALUES (3, 'doni', 'doni456', 'user', 'Doni Prasetyo', NULL)
    ''')

    cursor.execute('''
        INSERT OR IGNORE INTO secrets (id, secret_flag)
        VALUES (1, 'FLAG{B4ckup_D4t4b4s3_T3r3ksp0s}')
    ''')

    conn.commit()
    conn.close()
    print("Database initialized with flags.")

if __name__ == '__main__':
    init_db()
