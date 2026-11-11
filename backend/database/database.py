import sqlite3

DATABASE_NAME = "jobs.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TEXT
        )
    """)
    

    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN created_at TEXT
        """)

    except sqlite3.OperationalError:
        pass


    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN salary TEXT
        """)

    except sqlite3.OperationalError:
        pass


    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN url TEXT
        """)

    except sqlite3.OperationalError:
        pass


    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN contact TEXT
        """)

    except sqlite3.OperationalError:
        pass


    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN note TEXT
        """)

    except sqlite3.OperationalError:
        pass


    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN status TEXT DEFAULT 'Aktivní'
        """)
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("""
            ALTER TABLE jobs
            ADD COLUMN user_id INTEGER
        """)
        
    except sqlite3.OperationalError:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cv_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            text TEXT NOT NULL,
            ai_analysis TEXT NOT NULL,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            position TEXT NOT NULL,
            company TEXT,
            conversation TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()