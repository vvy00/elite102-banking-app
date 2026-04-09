from database import init_db
from accounts import create_account, get_account, list_accounts
from transactions import deposit, withdraw, get_history, transfer, apply_interest
from accounts import create_account, get_account, list_accounts, set_overdraft
from colorama import init, Fore, Style
init(autoreset=True)

def print_menu():
    print(Fore.CYAN + """
╔══════════════════════════════╗
║        Banking System        ║
╠══════════════════════════════╣
║  1. Create account           ║
║  2. Deposit                  ║
║  3. Withdraw                 ║
║  4. Check balance            ║
║  5. List all accounts        ║
║  6. Transaction history      ║
║  7. Wire Transfer            ║
║  8. Set overdraft limit      ║
║  9. Apply interest           ║
║  0. Exit                     ║
╚══════════════════════════════╝""")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(Fore.RED + "  Please enter a whole number.")

def get_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print(Fore.RED + "  Amount must be greater than zero.")
            else:
                return value
        except ValueError:
            print(Fore.RED + "  Please enter a valid amount (example: 50 or 50.00).")

def get_name(prompt):
    while True:
        name = input(prompt).strip()
        if len(name) == 0:
            print(Fore.RED + "  Name cannot be empty.")
        else:
            return name

def main():
    init_db()
    while True:
        print_menu()
        choice = input("  Choice: ").strip()

        if choice == "1":
            name = get_name("  Name: ")
            amt = get_float("  Initial deposit: $")
            acc_id = create_account(name, amt)
            print(Fore.GREEN + f"  Account #{acc_id} created for {name}!")

        elif choice == "2":
            acc_id = get_int("  Account ID: ")
            amt = get_float("  Deposit amount: $")
            try:
                deposit(acc_id, amt)
                print(Fore.GREEN + f"  Deposited ${amt:.2f} successfully.")
            except ValueError as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "3":
            acc_id = get_int("  Account ID: ")
            amt = get_float("  Withdraw amount: $")
            try:
                withdraw(acc_id, amt)
                print(Fore.GREEN + f"  Withdrew ${amt:.2f} successfully.")
            except ValueError as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "4":
            acc_id = get_int("  Account ID: ")
            acc = get_account(acc_id)
            if acc:
                print(Fore.YELLOW + f"  {acc['name']}: ${acc['balance']:.2f}")
            else:
                print(Fore.RED + "  Account not found.")

        elif choice == "5":
            accounts = list_accounts()
            if accounts:
                print(Fore.YELLOW + f"\n  {'ID':<5} {'Name':<20} {'Balance':>10}")
                print(Fore.YELLOW + "  " + "-" * 37)
                for a in accounts:
                    print(Fore.YELLOW + f"  {a['id']:<5} {a['name']:<20} ${a['balance']:>9.2f}")
            else:
                print(Fore.RED + "  No accounts yet.")

        elif choice == "6":
            acc_id = get_int("  Account ID: ")
            history = get_history(acc_id)
            if history:
                print(Fore.YELLOW + f"\n  {'Date':<20} {'Type':<10} {'Amount':>10}")
                print(Fore.YELLOW + "  " + "-" * 42)
                for t in history:
                    print(Fore.YELLOW + f"  {t['timestamp']:<20} {t['type']:<10} ${t['amount']:>9.2f}")
            else:
                print(Fore.RED + "  No transactions found.")

        elif choice == "7":
            print("  -- Wire Transfer --")
            from_id = get_int("  From account ID: ")
            to_id = get_int("  To account ID: ")
            amt = get_float("  Amount: $")
            try:
                transfer(from_id, to_id, amt)
                print(Fore.GREEN + f"  Transferred ${amt:.2f} from account #{from_id} to #{to_id}.")
            except ValueError as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "8":
            acc_id = get_int("  Account ID: ")
            limit = get_float("  Overdraft limit: $")
            try:
                set_overdraft(acc_id, limit)
                print(Fore.GREEN + f"  Overdraft limit set to ${limit:.2f} for account #{acc_id}.")
            except ValueError as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "9":
            rate = get_float("  Interest rate (%): ")
            try:
                apply_interest(rate)
                print(Fore.GREEN + f"  Interest of {rate}% applied to all accounts.")
            except ValueError as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "0":
            print(Fore.MAGENTA +"  Goodbye!")
            break

        else:
            print(Fore.RED + "  Invalid choice, try again.")

if __name__ == "__main__":
    main()