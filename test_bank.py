import unittest
import sqlite3
import database
from accounts import create_account, get_account, list_accounts
from transactions import deposit, withdraw, get_history

class TestBankApp(unittest.TestCase):

    def setUp(self):
        database.DB_PATH = ":memory:"
        database._conn = None
        database.init_db()

    def test_create_account(self):
        acc_id = create_account("Alice", 500)
        acc = get_account(acc_id)
        self.assertEqual(acc["name"], "Alice")
        self.assertAlmostEqual(acc["balance"], 500)

    def test_deposit(self):
        acc_id = create_account("Bob", 100)
        deposit(acc_id, 50)
        acc = get_account(acc_id)
        self.assertAlmostEqual(acc["balance"], 150)

    def test_withdraw_success(self):
        acc_id = create_account("Carol", 200)
        withdraw(acc_id, 75)
        acc = get_account(acc_id)
        self.assertAlmostEqual(acc["balance"], 125)

    def test_withdraw_insufficient_funds(self):
        acc_id = create_account("Dave", 50)
        with self.assertRaises(ValueError):
            withdraw(acc_id, 200)

    def test_negative_deposit_rejected(self):
        acc_id = create_account("Eve", 100)
        with self.assertRaises(ValueError):
            deposit(acc_id, -10)

    def test_transaction_history(self):
        acc_id = create_account("Frank", 300)
        deposit(acc_id, 100)
        withdraw(acc_id, 50)
        history = get_history(acc_id)
        self.assertEqual(len(history), 2)

if __name__ == "__main__":
    unittest.main()