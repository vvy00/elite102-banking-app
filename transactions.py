from database import get_connection

def deposit(account_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, account_id)
        )
        conn.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'deposit', ?)",
            (account_id, amount)
        )

def withdraw(account_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    conn = get_connection()
    account = conn.execute(
        "SELECT balance FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    if account is None:
        raise ValueError("Account not found")
    if account["balance"] < amount:
        raise ValueError("Insufficient funds")
    with conn:
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, account_id)
        )
        conn.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)",
            (account_id, amount)
        )

def get_history(account_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC",
        (account_id,)
    ).fetchall()
    conn.close()
    return rows

def transfer(from_id, to_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if from_id == to_id:
        raise ValueError("Cannot transfer to the same account")
    conn = get_connection()
    from_acc = conn.execute(
        "SELECT balance FROM accounts WHERE id = ?", (from_id,)
    ).fetchone()
    to_acc = conn.execute(
        "SELECT balance FROM accounts WHERE id = ?", (to_id,)
    ).fetchone()
    if from_acc is None:
        raise ValueError("Source account not found")
    if to_acc is None:
        raise ValueError("Destination account not found")
    if from_acc["balance"] < amount:
        raise ValueError("Insufficient funds")
    with conn:
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, from_id)
        )
        conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?",
            (amount, to_id)
        )
        conn.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer out', ?)",
            (from_id, amount)
        )
        conn.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'transfer in', ?)",
            (to_id, amount)
        )

def withdraw(account_id, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    conn = get_connection()
    account = conn.execute(
        "SELECT balance, overdraft_limit FROM accounts WHERE id = ?", (account_id,)
    ).fetchone()
    if account is None:
        raise ValueError("Account not found")
    available = account["balance"] + account["overdraft_limit"]
    if available < amount:
        raise ValueError(f"Insufficient funds. Available balance including overdraft: ${available:.2f}")
    with conn:
        conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?",
            (amount, account_id)
        )
        conn.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'withdraw', ?)",
            (account_id, amount)
        )

def apply_interest(rate):
    if rate <= 0:
        raise ValueError("Interest rate must be positive")
    conn = get_connection()
    accounts = conn.execute("SELECT id, balance FROM accounts").fetchall()
    with conn:
        for account in accounts:
            if account["balance"] > 0:
                interest = round(account["balance"] * (rate / 100), 2)
                conn.execute(
                    "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                    (interest, account["id"])
                )
                conn.execute(
                    "INSERT INTO transactions (account_id, type, amount) VALUES (?, 'interest', ?)",
                    (account["id"], interest)
                )
    print(f"  Interest of {rate}% applied to all accounts.")