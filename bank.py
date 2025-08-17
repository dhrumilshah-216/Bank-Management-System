import json
import re
import random
import string
from datetime import datetime
from pathlib import Path

class Bank:

    database = 'data.json'
    data = []

    try:
        if(Path(database).exists()):
            with open(database, 'r') as f:
                data = json.loads(f.read())

    except Exception as e:
        print(f"Exception occured as {e}")
    
    @staticmethod
    def __update():
        with open(Bank.database, 'w') as f:
            json.dump(Bank.data, f, indent=4)

    @classmethod
    def __accnumgen(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        schar = random.choices("!@#$%&*~", k=1)
        id = alpha + num + schar
        random.shuffle(id)
        return "".join(id)

    def createaccount(self):
        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "phone_number": int(input("Enter your permanent Phone number: ")),
            "email": input("Enter your permanent E-mail: "),
            "pin": int(input("Enter your Pin: ")),
            "account_no": Bank.__accnumgen(),
            "balance": 0
        }
        if(info["age"] <= 18):
            print("Sorry, You are under aged.\nYour account cannot be created.")
            return

        if not info["name"].replace(" ", "").isalpha():
            print(f"Your name {info['name']} is not valid")
            return

        if(len(str(info["phone_number"]))) != 10:
            print(f"Your Phone Number {info['phone_number']} contains {len(str(info['phone_number']))} digits")
            return

        if(not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', info['email'])):
            print(f"Your E-mail id {info['email']} is not valid")
            return

        if(len(str(info["pin"]))) != 4:
            print("Your pin must contain 4 digits")
            return
        
        print("Account created successfully!")
        for i in info:
            print(f"{i}: {info[i]}")
        print("Please note down your account number")
        Bank.data.append(info)
        Bank.__update()

    def depositmoney(self):
        account_no = input("Enter your account number: ")
        pin = int(input("Enter your pin: "))

        userdata = [i for i in Bank.data if i['account_no'] == account_no and i['pin'] == pin]

        if userdata == []:
            print("Please enter correct account no. and pin.")

        else:
            amount = int(input("Enter the amount you want to deposit: "))

            if amount <= 0 or amount > 10000:
                print("You can only deposit between 0 and 10000")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print(f"Congratulations! {amount} Rs. are deposited successfully in your bank account")

    def withdrawmoney(self):
        account_no = input("Enter your account number: ")
        pin = int(input("Enter your pin: "))

        userdata = [i for i in Bank.data if i['account_no'] == account_no and i['pin'] == pin]

        if userdata == []:
            print("Please enter correct account no. and pin.")

        else:
            amount = int(input("Enter the amount you want to withdraw: "))

            if userdata[0]['balance'] < amount:
                print("Not enough money in account")
            elif amount <= 0 or amount > 10000:
                print("You can only withdraw between 0 and 10000")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print(f"Congratulations! {amount} Rs. are withdrawed successfully from your bank account")

    def transfermoney(self):
        # Sender details
        sender_acc = input("Enter your account number: ")
        sender_pin = int(input("Enter your pin: "))

        sender_data = [i for i in Bank.data if i['account_no'] == sender_acc and i['pin'] == sender_pin]

        if sender_data == []:
            print("Please enter correct account no. and pin.")
            return

        # Recipient details
        recipient_acc = input("Enter recipient's account number: ")
        recipient_data = [i for i in Bank.data if i['account_no'] == recipient_acc]

        if recipient_data == []:
            print("Recipient account not found.")
            return

        if sender_acc == recipient_acc:
            print("Cannot transfer money to the same account.")
            return

        # Transfer amount
        amount = int(input("Enter the amount you want to transfer: "))

        if amount <= 0 or amount > 10000:
            print("You can only transfer between 1 and 10000")
            return

        if sender_data[0]['balance'] < amount:
            print("Insufficient balance for transfer")
            return

        # Perform transfer
        sender_data[0]['balance'] -= amount
        recipient_data[0]['balance'] += amount
        Bank.__update()
        
        print(f"Transfer successful!")
        print(f"Transferred {amount} Rs. to {recipient_data[0]['name']}")
        print(f"Your remaining balance: {sender_data[0]['balance']} Rs.")

    def showdetails(self):
        account_no = input("Enter your account number: ")
        pin = int(input("Enter your pin: "))

        userdata = [i for i in Bank.data if i['account_no'] == account_no and i['pin'] == pin]

        if userdata == []:
            print("Please enter correct account no. and pin.")

        else:
            print("Your information is:")
            for i in userdata[0]:
                print(f"{i}: {userdata[0][i]}")

    def updatedetails(self):
        account_no = input("Enter your account number: ")
        pin = int(input("Enter your pin: "))

        userdata = [i for i in Bank.data if i['account_no'] == account_no and i['pin'] == pin]
        # print(userdata)
        if userdata == []:
            print("Please enter correct account no. and pin.")

        else:
            print("Please fill the following details if want to change or leave it empty for no change")

            newdata = {
                "name": input("Enter your new name if there are any changes or press enter to skip: "),
                "age": userdata[0]['age'],
                "phone_number": input("Enter your new Phone Number if there are any changes or press enter to skip: "),
                "email": input("Enter your new E-mail if there are any changes or press enter to skip: "),
                "pin": input("Enter your new pin if there are any changes or press enter to skip: "),
                "account_no": userdata[0]['account_no'],
                "balance": userdata[0]['balance']
            }

            if newdata["name"] == "":
                newdata["name"] = userdata[0]['name']
            else:
                if not newdata["name"].replace(" ", "").isalpha():
                    print(f"Your name {newdata['name']} is not valid")
                    return
                
            if newdata["phone_number"] == "":
                newdata["phone_number"] = userdata[0]['phone_number']
            else:
                if(not newdata["phone_number"].isdigit()) or (len(newdata["phone_number"]) != 10):
                    print(f"Your Phone Number {newdata['phone_number']} is not valid")
                    return
                else:
                    newdata["phone_number"] = int(newdata["phone_number"])
                
            if newdata["email"] == "":
                newdata["email"] = userdata[0]['email']
            else:
                if(not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', newdata['email'])):
                    print(f"Your E-mail id {newdata['email']} is not valid")
                    return
                
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]['pin']
            else:
                if(not newdata["pin"].isdigit()) or (len(newdata["pin"]) != 4):
                    print(f"Your pin {newdata['pin']} is not valid")
                    return
                else:
                    newdata["pin"] = int(newdata["pin"])
            
            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]
            Bank.__update()
            print("Congratulations! Details updated successfully")

    def deleteaccount(self):
        account_no = input("Enter your account number: ")
        pin = int(input("Enter your pin: "))

        userdata = [i for i in Bank.data if i['account_no'] == account_no and i['pin'] == pin]
        # print(userdata)
        if userdata == []:
            print("Please enter correct account no. and pin.")

        else:
            acc = Bank.data.index(userdata[0])
            Bank.data.pop(acc)
            Bank.__update()
            print("Your account is deleted successfully!")

    @classmethod
    def login(cls, acc_no, pin):
        for i, u in enumerate(cls.data):
            if u["account_no"] == acc_no and u["pin"] == pin:
                return cls.data[i]  # ✅ this returns actual reference
        return None

    @classmethod
    def find_user_by_account(cls, account_no):
        """Find user by account number for transfers"""
        for user in cls.data:
            if user["account_no"] == account_no:
                return user
        return None

    @classmethod
    def update_user_balance(cls, account_no, new_balance):
        """Update user balance by account number"""
        for user in cls.data:
            if user["account_no"] == account_no:
                user["balance"] = new_balance
                cls.__update()
                return True
        return False

    @classmethod
    def get_all_accounts(cls):
        """Get all account numbers and names for admin purposes"""
        return [(user["account_no"], user["name"]) for user in cls.data]
    
    