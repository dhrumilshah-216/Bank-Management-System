# from bank import Bank
import json
import re
import random
import string
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
            print("Please fill the follo0wing details if want to change or leave it empty for no change")

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

def show_menu():
    print('''
0 - Exit
1 - Create an account
2 - Deposit money
3 - Withdraw money
4 - See account details
5 - Update details
6 - Delete account
''')

user = Bank()

while True:
    show_menu()
    command = input("Enter your command: ").strip()
    print()

    if command == "1":
        user.createaccount()

    elif command == "2":
        user.depositmoney()

    elif command == "3":
        user.withdrawmoney()

    elif command == "4":
        user.showdetails()

    elif command == "5":
        user.updatedetails()

    elif command == "6":
        while True:
            confirmation = input("Are you sure you want to delete your account?\n1 - Yes\n2 - No\n→ ").strip()
            if confirmation == "1":
                user.deleteaccount()
                break
            elif confirmation == "2":
                print("Deletion cancelled.\n")
                break
            else:
                print("Invalid input. Please enter 1 or 2.\n")

    elif command == "0":
        print("Exiting. Thank you!")
        break

    else:
        print("Invalid command. \nPlease try again....\n")
