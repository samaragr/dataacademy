import os
import csv
from .User import User
from .ChequeAccount import ChequeAccount
from .SavingsAccount import SavingsAccount


class ATM:
    # Loads data from data directory into lists. A temporary list is created in order to change "|||" to "|"
    # so the csv method can be used as delimiter must be 1 char
    def __init__(self, userinfo_file, accounts_file):
        self.userinfo_file = os.path.join(os.getcwd(), userinfo_file)
        self.accounts_file = os.path.join(os.getcwd(), accounts_file)
        self.users = []
        self.accounts = []
        self.transacting_account = None
        with open(self.userinfo_file) as load_file:
            reader = csv.DictReader(load_file, delimiter=",")
            for row in reader:
                new_user = User(row["FirstName"], row["Surname"], row["Mobile"], row["AccountOwnerID"])
                self.users.append(new_user)

        raw_accounts = []
        with open(self.accounts_file) as load_file:
            for line in load_file:
                line = line.replace("|||", "|")
                raw_accounts.append(line)

        reader = csv.DictReader(raw_accounts, delimiter="|")
        new_account = None
        for row in reader:
            if row["AccountType"] == "Cheque":
                new_account = ChequeAccount(row["AccountOwnerID"], row["AccountNumber"], row["OpeningBalance"])
            if row["AccountType"] == "Saving":
                new_account = SavingsAccount(row["AccountOwnerID"], row["AccountNumber"], row["OpeningBalance"])
            self.accounts.append(new_account)

    def run(self):
        """Runs the ATM program"""
        choice = None
        while choice != "q":
            print("Please enter your User ID:")
            userid = input()
            current_user = None
            for user in self.users:
                if userid == user.id:
                    current_user = user
                    break
            if current_user is None:
                print("Wrong input. Invalid user ID")
                continue
            user_accounts = self.get_user_accounts(current_user)
            welcome_msg = """
    Welcome {}. Please enter an Option
        1 For Deposit
        2 For Withdraw
        3 For Balance
        q To Quit""".format(str(current_user))
            print(welcome_msg)
            choice = input()
            if choice == "1":
                self.deposit(user_accounts)
            elif choice == "2":
                self.withdrawal(user_accounts)
            elif choice == "3":
                self.balance(user_accounts)
            elif choice != "q":
                print("Wrong input. Invalid transaction option")
        if choice == "q":
            for account in user_accounts:
                print(str(account) + ":\t$" + str(account.balance))
            self.save_accounts()

    def save_accounts(self):
        """Writes new account info back to file in original format"""
        with open(self.accounts_file, "w") as load_file:
            load_file.write("AccountOwnerID|||AccountNumber|||AccountType|||OpeningBalance")
            for account in self.accounts:
                load_file.write("\n{0}|||{1}|||{2}|||{3}".format
                                (account.owner, account.number, account.type, round(account.balance, 2)))

    def get_user_accounts(self, user):
        """returns list of accounts associated with current user"""
        user_accounts = []
        for account in self.accounts:
            if user.id == account.owner:
                user_accounts.append(account)
        return user_accounts

    def get_account_options(self, accounts):
        """Prints all user accounts for the current user"""
        account_options = ""
        n = 1
        for account in accounts:
            account_option = "\n\t {0} for {1}".format(n, str(account))
            account_options += account_option
            n += 1
        return account_options

    def deposit(self, accounts):
        """Prompts for an account to deposit into. If it exists moves to deposit transaction method"""
        account_options = self.get_account_options(accounts)
        deposit_msg = "Which account do you wish to deposit to:" + account_options
        print(deposit_msg)
        account_choice = int(input()) - 1
        if account_choice > len(accounts) - 1 or account_choice < 0:
            print("Wrong input. Invalid account choice")
        else:
            self.transacting_account = accounts[account_choice]
            self.deposit_amount()

    def deposit_amount(self):
        print("How much do you wish to deposit?")
        deposit_amount = float(input())
        self.transacting_account.balance += deposit_amount

    def withdrawal(self, accounts):
        """Prompts for an account to withdraw from. If it exists moves to withdrawal transaction method"""
        account_options = self.get_account_options(accounts)
        withdrawal_msg = "Which account do you wish to withdraw from:" + account_options
        print(withdrawal_msg)
        account_choice = int(input()) - 1
        if account_choice > len(accounts) - 1 or account_choice < 0:
            print("Wrong input. Invalid account choice")
        else:
            self.transacting_account = accounts[account_choice]
            self.withdrawal_amount()

    def withdrawal_amount(self):
        print("How much do you wish to withdraw? Balance = $" + str(self.transacting_account.balance))
        withdrawal_amount = float(input())
        if withdrawal_amount > self.transacting_account.balance:
            print("Error: Wrong input. Amount entered (${0}) is greater than amount in account".format
                  (withdrawal_amount))
        else:
            self.transacting_account.balance -= withdrawal_amount
        print("Your new balance for " + str(self.transacting_account) + " is $" + str(self.transacting_account.balance))

    def balance(self, accounts):
        account_options = self.get_account_options(accounts)
        balance_msg = "Which account do you wish to view?" + account_options
        print(balance_msg)
        account_choice = int(input()) - 1
        if account_choice > len(accounts) - 1 or account_choice < 0:
            print("Wrong input. Invalid account choice")
        else:
            transacting_account = accounts[account_choice]
            print("Current balance for account " + str(transacting_account) + ": $" + str(transacting_account.balance))


if __name__ == "__main__":
    ourATM = ATM('data/UserInfo.txt', 'data/OpeningAccountsData.txt')
    ourATM.run()
