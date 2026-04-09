import sqlite3

DB_PATH = "bank.db"
_conn = None

def get_connection():
    global _conn, DB_PATH
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        _conn.row_factory = sqlite3.Row
    return _conn

def init_db():
    global _conn, DB_PATH
    _conn = sqlite3.connect(DB_PATH)
    _conn.row_factory = sqlite3.Row
    with _conn:
        _conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT    NOT NULL,
                balance REAL    NOT NULL DEFAULT 0.0,
                created TEXT    DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS transactions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                type       TEXT    NOT NULL,
                amount     REAL    NOT NULL,
                timestamp  TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
            CREATE TABLE IF NOT EXISTS accounts (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                name           TEXT    NOT NULL,
                balance        REAL    NOT NULL DEFAULT 0.0,
                overdraft_limit REAL   NOT NULL DEFAULT 0.0,
                created        TEXT    DEFAULT (datetime('now'))
            );
        """)
    print("Database ready!")