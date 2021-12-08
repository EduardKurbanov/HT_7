"""
1. Програма-банкомат.

   Створити програму з наступним функціоналом:

      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);

      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) та історію транзакцій (файл <{username}_transactions.data>);

      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено число; знімається не більше, ніж є на рахунку).

   Особливості реалізації:

      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);

      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;

      - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)

   Особливості функціонала:

      - за кожен функціонал відповідає окрема функція;

      - основна функція - <start()> - буде в собі містити весь workflow банкомата:

      - спочатку - логін користувача - програма запитує ім'я/пароль. Якщо вони неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )

      - потім - елементарне меню типа:

        Введіть дію:

           1. Продивитись баланс

           2. Поповнити баланс

           3. Вихід

      - далі - фантазія і креатив :)
"""

import csv
import json
import time


class LoginException(Exception):
    pass


class PasswordException(Exception):
    pass


def verification_password_login(username="", password=""):
    with open("users.csv", "r", ) as file_user:

        reader = csv.DictReader(file_user)
        list_of_stuff = []
        for i in reader:
            list_of_stuff.append(i)
        data = {}
        for i in list_of_stuff:
            data[i["login"]] = i["password"]
        try:
            if username in data.keys():
                if password in data.values():
                    return True
                else:
                    raise PasswordException(f"incorrect password -> {password}")
            else:
                raise LoginException(f"incorrect login -> {username}")
        except LoginException as err:
            print(f"starus incorrect login -> {err}")
        except PasswordException as err:
            print(f"status incorrect password -> {err}")


def check_balance(username: str):
    try:
        file = open("{0}_balance.data".format(username), "r")
        money = file.read()
    except IOError:
        raise IOError("File does not appear to exist.")

    print("Balance: {0} USD".format(money))
    file.close()


def replenish_balance(username: str):
    transaction_set = {}

    with open("{0}_balance.data".format(username)) as balance_file:
        current_balance = balance_file.read()

    print("Balance: {0} USD".format(current_balance))  # for debug only
    entered_money = input("Enter amount : ")
    if entered_money.isdecimal():
        if (int(entered_money) != 0):
            new_balance = int(current_balance) + int(entered_money)
            print("Balance: {0} USD".format(new_balance))

            with open("{0}_balance.data".format(username), "w") as balance_file:
                balance_file.write(str(new_balance))

            with open("{0}_transactions.data".format(username)) as transaction_file:
                data = list(json.load(transaction_file))

            transaction_set = {"timestamp": int(time.time()), "old_balance": current_balance,
                               "new_balance": new_balance, "replenished": int(entered_money)}
            data.append(transaction_set)

            with open("{0}_transactions.data".format(username), "w") as js_file:
                json.dump(data, js_file, indent=4)
        else:
            print("Entered incorrect amount")
    else:
        print("Only digits allowed to enter")


def withdraw_balance(username: str):
    transaction_set = {}

    with open("{0}_balance.data".format(username)) as balance_file:
        current_balance = balance_file.read()

    print("Balance: {0} USD".format(current_balance))  # for debug only
    entered_money = input("Enter amount : ")
    if entered_money.isdecimal():
        if (int(entered_money) != 0) and (int(entered_money) <= int(current_balance)):
            new_balance = int(current_balance) - int(entered_money)
            print("Balance: {0} USD".format(new_balance))

            with open("{0}_balance.data".format(username), "w") as balance_file:
                balance_file.write(str(new_balance))

            with open("{0}_transactions.data".format(username)) as transaction_file:
                data = list(json.load(transaction_file))

            transaction_set = {"timestamp": int(time.time()), "old_balance": current_balance,
                               "new_balance": new_balance, "withdraw": int(entered_money)}
            data.append(transaction_set)

            with open("{0}_transactions.data".format(username), "w") as js_file:
                json.dump(data, js_file, indent=4)
        else:
            print("Entered incorrect amount")
    else:
        print("Only digits allowed to enter")


def start():
    count = 3
    while True:
        try:
            login = input("enter login: ")
            password = input("enter password: ")
            valid = verification_password_login(login, password)
            while count > 0:
                if valid:
                    print("1. Look at the balance")
                    print("2. Replenish the balance")  # пополнить счет
                    print("3. Withdraw cash")  # снять наличные
                    print("4. Exit")
                    menu_item = input("Choose : ")
                    if int(menu_item) == 1:
                        check_balance(login)
                    elif int(menu_item) == 2:
                        replenish_balance(login)
                    elif int(menu_item) == 3:
                        withdraw_balance(login)
                    else:
                        exit()
                else:
                    count -= 1
                    print(f"attempt -> {count}")
                    break

                if count > 0:
                    continue
                else:
                    print("exit the program automatically")
            if count == 0:
                break

        except Exception as err:
            print(f"error -> {err}")


# if __name__ in "__main__":
start()
