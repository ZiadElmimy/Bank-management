import csv
import random
from datetime import datetime

class Account:
    def __init__(self, name, card_type, balance = 0):
        self.balance = balance
        self.name = name
        self.card_type = card_type

    def __str__(self):
        name_sentence = f"\nYour account initiated with the name '{self.name}'\n"
        card_type_sentence = f"Card type is {self.card_type}\n"
        return name_sentence + card_type_sentence

    @classmethod
    def Init_Account(cls):
        _name = input("Name: ")
        _card_type = input("Card type [Visa, Master Card]: ")
        if _card_type not in ["Visa", "Master Card"]:
            raise ValueError("Invalid card")
        
        return cls(_name, _card_type)

class Card(Account):
    def __init__(self, name, card_type, balance, card_num, status, end_date, password, security_code):
        super().__init__(name, card_type, balance)
        self.card_num = card_num
        self.status = status
        self.end_date = end_date
        self.password = password
        self.security_code = security_code

    def __str__(self):
        card_sentence = f"Your card number is: {self.card_num} with {self.security_code} as a security code\n"
        validity_sentence = f"Valid until {self.end_date}\n"
        return card_sentence + validity_sentence

    @classmethod
    def Generate_Card(cls, name, card_type):
        _card = ""
        __card = []

        if card_type == "Visa":
            c = 15
            __card.append("4")
            while c > 0:
                __card.append(str(random.randint(0, 9)))
                c -= 1
            _card = ''.join(__card)
        
        elif card_type == "Master Card":
            c = 14
            __card.append(str(random.randint(51, 55)))
            while c > 0:
                __card.append(str(random.randint(0, 9)))
                c -= 1
            _card = ''.join(__card)

        while True:
            try:
                _password_test = input("Password (4 digits): ")
                if len(_password_test) != 4 or not _password_test.isdigit():
                    print("The password must be 4 digits")
                    continue
                _password = int(_password_test)
                break
            except ValueError:
                print("Your password contains at least one non-numerical digit")
                continue

        _status = "Normal"
        _year, _mon = (datetime.today().strftime("%y-%m")).split("-")
        _end_date = f"{str(int(_year) + 5)}-{_mon}"
        _security_code = str(random.randint(100, 999))

        return cls(name, card_type, 0, _card, _status, _end_date, _password, _security_code)

class Client:

    fields = ["name", "card_type", "balance", "card_num", "status", "end_date", "password", "security_code"]

    def __str__(self):
        return "The account opened successfully"

    @classmethod
    def Open_account(cls):
        account = Account.Init_Account()
        card = Card.Generate_Card(account.name, account.card_type)

        client_info = {
            "name" : (card.name).rstrip(),
            "card_type" : card.card_type,
            "balance" : card.balance,
            "card_num" : card.card_num,
            "status" : card.status,
            "end_date" : card.end_date,
            "password" : card.password,
            "security_code" : card.security_code
        }

        with open("accounts.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.fields)
            writer.writerow(client_info)

    
    @classmethod
    def Deposit(cls, card_num, password, amount):
        info = []
        client = {}

        with open("accounts.csv") as file:
            reader = csv.DictReader(file)

            for record in reader:
                if record["card_num"] == card_num and record["password"] == password:
                    client = record
                    _balance = int(record["balance"])
                    _balance += amount
                    record["balance"] = str(_balance)

                info.append(record)

            if not client:
                raise ValueError("your account isn't found")  
            
            print("------------------------------")
            print("your deposit done successfully with", str(amount) + "$", "MR/MS.", client["name"], end="\n")

        with open("accounts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.fields)

            writer.writeheader()
            writer.writerows(info)

    @classmethod
    def Withdraw(cls, card_num, password, amount):

        info = []
        client = {}

        with open("accounts.csv") as file:
            reader = csv.DictReader(file)

            for record in reader:
                if record["card_num"] == card_num and record["password"] == password:
                    client = record
                    if amount <= int(record["balance"]):
                        _balance = int(record["balance"])
                        _balance -= amount
                        record["balance"] = str(_balance)
                    else:
                        raise ValueError("There is no enough money to withdraw")    
                info.append(record)

            if not client:
                raise ValueError("your account isn't found")   

        print("------------------------------")
        print("your withdrawal done successfully with", str(amount) + "$", "MR/MS.", client["name"], end="\n")

        with open("accounts.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames= cls.fields)

            writer.writeheader()
            writer.writerows(info)

    @classmethod
    def Check_balance(cls, card_num, password):
        
        with open("accounts.csv") as file:
            reader = csv.DictReader(file)

            for record in reader:
                if record["card_num"] == card_num and record["password"] == password:
                    return record["balance"]
                else:
                    print("your account isn't found")
        




def main():
    # initiate an account
    Client.Open_account()

    #deposit and withdraw from the account
    Client.Deposit("5371431410975570", "1920", 2000) # deposite for Mohamed's account
    Client.Deposit("5469294102230371", "1207", 1400) # deposite for Ziad's account
    Client.Deposit("4460372469442497", "2003", 200) # deposite for Aya's account
    Client.Deposit("4460372469442497", "2003", 600) # deposite for Aya's account again

    # check the balance of Ziad's account
    balance = Client.Check_balance("5469294102230371", "1207")
    print("\n>> the balance in Ziad's account", balance)

    # withdraw from Ziad's account
    Client.Withdraw("5469294102230371", "1207", 500) # withdraw for Ziad's account

    # check the balance of Ziad's account
    balance = Client.Check_balance("5469294102230371", "1207")
    print("\n>> the balance in Ziad's account", balance)




if __name__ == "__main__":
    main()
