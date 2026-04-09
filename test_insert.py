import sqlite3

conn = sqlite3.connect('bank.db')

# Make a deposit
conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (50, 1))
conn.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (1, "deposit", 50))
conn.commit()

# Make a withdrawal
conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (30, 1))
conn.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (1, "withdraw", 30))
conn.commit()

# Read the transaction history
rows = conn.execute("SELECT * FROM transactions WHERE account_id = 1").fetchall()
print("Transaction history for account 1:")
for row in rows:
    print(" ", row[2], "$" + str(row[3]), "at", row[4])

conn.close()