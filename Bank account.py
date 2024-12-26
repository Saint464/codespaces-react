import hashlib
import getpass

class BankAccount:
    def __init__(self, account_number, balance, pin):
        self.account_number = account_number
        self.balance = balance
        self.pin = hashlib.sha256(pin.encode()).hexdigest()

    def get_balance(self):
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        self.balance -= amount
        return True

    def deposit(self, amount):
        self.balance += amount

    def authenticate(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest() == self.pin

class Card:
    def __init__(self, card_number, balance):
        self.card_number = card_number
        self.balance = balance

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        self.balance -= amount
        return True

class CardReaderWriter:
    def transfer_funds_from_account(self, account, card, amount):
        if amount <= account.get_balance():
            account.withdraw(amount)
            card.deposit(amount)
            return True
        else:
            return False

    def write_card_data(self, card, new_balance):
        # Simulates writing data to a cloned card
        card.balance = new_balance
        print(f"Card data updated successfully. New balance: ${card.get_balance()}")

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, balance, pin):
        self.accounts[account_number] = BankAccount(account_number, balance, pin)

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def create_card(self, card_number, balance):
        return Card(card_number, balance)

def main():
    bank_system = BankSystem()

    # Create mock bank account
    account_number = "123456789"
    balance = 1000000
    pin = "4201"
    bank_system.create_account(account_number, balance, pin)

    # Create card
    card_number = "987654321"
    card_balance = 0
    card = bank_system.create_card(card_number, card_balance)

    card_reader_writer = CardReaderWriter()

    while True:
        print("\nMenu:")
        print("1. Check account balance")
        print("2. Withdraw from account")
        print("3. Deposit to account")
        print("4. Transfer to card")
        print("5. Check card balance")
        print("6. Update card balance (Clone Card Writer)")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            account = bank_system.get_account(account_number)
            if account:
                print(f"Account balance: ${account.get_balance():.2f}")
            else:
                print("Account not found")

        elif choice == "2":
            account = bank_system.get_account(account_number)
            if account:
                amount = float(input("Enter amount to withdraw: "))
                if account.withdraw(amount):
                    print("Withdrawal successful")
                else:
                    print("Withdrawal failed")
            else:
                print("Account not found")

        elif choice == "3":
            account = bank_system.get_account(account_number)
            if account:
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
                print("Deposit successful")
            else:
                print("Account not found")

        elif choice == "4":
            account = bank_system.get_account(account_number)
            if account:
                pin = getpass.getpass("Enter PIN: ")
                if account.authenticate(pin):
                    amount = float(input("Enter amount to transfer: "))
                    if card_reader_writer.transfer_funds_from_account(account, card, amount):
                        print("Transfer successful")
                    else:
                        print("Transfer failed")
                else:
                    print("Authentication failed")
            else:
                print("Account not found")

        elif choice == "5":
            print(f"Card balance: ${card.get_balance():.2f}")

        elif choice == "6":
            new_balance = float(input("Enter new card balance: "))
            card_reader_writer.write_card_data(card, new_balance)

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()