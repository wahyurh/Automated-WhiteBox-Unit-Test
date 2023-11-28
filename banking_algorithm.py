import random
import shelve

def generate_account_number():
    return str(random.randint(10000, 99999))

def create_bank_account(account_balances, account_credentials):
    account_number = generate_account_number()
    deposit = float(input("Masukan Deposit pertama: "))
    account_balances[account_number] = deposit

    # Create login credentials
    username = input("Masukkan username untuk akun Anda: ")
    password = input("Masukkan password untuk akun Anda: ")
    account_credentials[account_number] = {'username': username, 'password': password}

    print(f"Account berhasil dibuat. Nomer Rekening Anda: {account_number}")

def login(account_credentials):
    account_number = input("Enter your account number: ")
    if account_number in account_credentials:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if (
                username == account_credentials[account_number]['username'] and
                password == account_credentials[account_number]['password']
        ):
            return account_number
        else:
            print("Invalid username or password. Please try again.")
            return None
    else:
        print("Invalid account number. Please create an account first.")
        return None

def deposit(account_balances, account_number):
    deposit_amount = float(input("Enter deposit amount: "))
    if deposit_amount < 0:
        print("Deposit amount cannot be negative.")
    else:
        account_balances[account_number] += deposit_amount
        print("Deposit successful.")

# Function to perform a withdrawal
def withdrawal(account_balances, account_number):
    withdrawal_amount = float(input("Enter withdrawal amount: "))
    if withdrawal_amount < 0:
        print("Withdrawal amount cannot be negative.")
    elif withdrawal_amount < 50000 or withdrawal_amount % 5000 != 0:
        print("Invalid withdrawal amount. Minimum withdrawal is 50000 and must be a multiple of 5000.")
    elif account_balances[account_number] >= withdrawal_amount:
        # Deduct the withdrawal amount and administration fee
        account_balances[account_number] -= (withdrawal_amount + 2500)
        print("Withdrawal successful.")
    else:
        print("Insufficient funds.")

# Function to check account balance
def check_balance(account_balances, account_number):
    print(f"Your account balance is: ${account_balances[account_number]:.2f}")

# Function to transfer money to another account
def transfer(account_balances, account_credentials, sender_account):
    destination_account = input("Enter the destination account number: ")
    amount = float(input("Enter the amount to transfer: "))

    if destination_account in account_balances:
        # Check if there are sufficient funds for the transfer
        if amount < 0:
            print("Transfer amount cannot be negative.")
        elif account_balances[sender_account] >= (amount + 2500):
            # Deduct the amount and administration fee from the sender's account
            account_balances[sender_account] -= (amount + 2500)
            # Add the amount to the destination account
            account_balances[destination_account] += amount

            # Get the usernames of both sender and receiver
            sender_username = account_credentials[sender_account]['username']
            receiver_username = account_credentials[destination_account]['username']

            print(f"Transfer successful. ${amount:.2f} transferred from {sender_username}'s account to {receiver_username}'s account.")
        else:
            print("Insufficient funds for the transfer.")
    else:
        print("Destination account does not exist.")

# Main function
def main():
    # Open the shelf files for persistent storage
    with shelve.open("bank_accounts") as account_balances, shelve.open("account_credentials") as account_credentials:
        print("\nBanking Menu:")
        print("1. Create Bank Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            create_bank_account(account_balances, account_credentials)
        elif choice == '2':
            account_number = login(account_credentials)
            if account_number is not None:
                print("\nBanking Options:")
                print("1. Deposit")
                print("2. Withdrawal")
                print("3. Check Account Balance")
                print("4. Transfer")

                banking_choice = input("Enter your choice (1-4): ")

                if banking_choice == '1':
                    deposit(account_balances, account_number)
                elif banking_choice == '2':
                    withdrawal(account_balances, account_number)
                elif banking_choice == '3':
                    check_balance(account_balances, account_number)
                elif banking_choice == '4':
                    transfer(account_balances, account_credentials, account_number)
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
        elif choice == '3':
            print("Exiting the banking program. Goodbye!")

if __name__ == "__main__":
    main()
