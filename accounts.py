from database import get_connection

def create_account(name, initial_deposit=0.0):
    if initial_deposit < 0:
        raise ValueError("Initial deposit cannot be negative")
    conn = get_connection()
    with conn:
        cursor = conn.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)",
            (name, initial_deposit)
        )
        return cursor.lastrowid

def get_account(account_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    conn.close()
    return row

def list_accounts():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM accounts ORDER BY id").fetchall()
    conn.close()
    return rows

def set_overdraft(account_id, limit):
    if limit < 0:
        raise ValueError("Overdraft limit cannot be negative")
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE accounts SET overdraft_limit = ? WHERE id = ?",
            (limit, account_id)
        )
    print(f"  Overdraft limit set to ${limit:.2f} for account #{account_id}")