import sqlite3
import os
import base64

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
            fullname TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_secret INTEGER DEFAULT 0,
            FOREIGN KEY (owner_id) REFERENCES users(id)
        )
    ''')

    users = [
        (1, 'ceo', 'ceo123', 'admin', 'Alex Johnson (CEO)'),
        (2, 'manager', 'manager123', 'manager', 'Sarah Lee (Manager)'),
        (3, 'user1', 'user123', 'user', 'Budi Santoso'),
        (4, 'user2', 'user456', 'user', 'Dewi Permata')
    ]
    cursor.executemany('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)', users)

    documents = [
        (1, 1, 'Strategic Plan 2026', 'This is the company strategy... Flag: FLAG{1D0R_brut3f0rc3_b64}', 1),
        (2, 1, 'Salary List', 'CEO: $200k, Manager: $120k, Staff: $60k', 1),
        (3, 2, 'Project Timeline Q2', 'Launch date: June 1st', 0),
        (4, 2, 'Team Evaluation', 'Budi: Good performance', 0),
        (5, 3, 'Personal Notes', 'My tasks: fix bug #123', 0),
        (6, 4, 'Meeting Minutes', 'Discuss new feature', 0)
    ]
    cursor.executemany('INSERT OR IGNORE INTO documents VALUES (?,?,?,?,?)', documents)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    cursor.execute('INSERT OR IGNORE INTO config VALUES (?, ?)', ('flag2', 'FLAG{Debu9_3ndp0int_T3rbuk4}'))

    conn.commit()
    conn.close()
    print("Database initialized with advanced data.")

if __name__ == '__main__':
    init_db()
