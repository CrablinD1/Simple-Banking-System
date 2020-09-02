import random
import sqlite3

conn = sqlite3.connect("card.s3db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS card
                  (id INTEGER, number text, pin text,
                   balance INTEGER DEFAULT 0)
               """)
sql = "SELECT * FROM card"
cursor.execute(sql)
card_id = len(cursor.fetchall())


class Card:
    def __init__(self, card_id=card_id):
        BIN = str(random.randrange(400000000000000, 400000999999999))
        self.number = BIN + str(luhn_algorithm(BIN))
        self.pin = str(random.randint(0, 9999)).zfill(4)
        self.balance = 0
        card_id += 1
        sqlin = "INSERT INTO card VALUES (?, ?, ?, ?)"
        cursor.execute(sqlin, [card_id, self.number, self.pin, self.balance])
        conn.commit()

    def get_balance(self):
        return self.balance

    def init_info(self):
        print("Your card has been created",
              "Your card number:",
              self.number,
              "Your card PIN:",
              self.pin, sep="\n")


def login():
    global ent_card_number
    ent_card_number = input('Enter your card number:')
    ent_card_PIN = input('Enter your PIN:')
    cmd = "SELECT pin FROM card WHERE  number = '{}'".format(ent_card_number)
    cursor.execute(cmd)
    results = cursor.fetchone()
    if results is None:
        print('Wrong card number or PIN')
        return False
    if ent_card_PIN != results[0]:
        print('Wrong card number or PIN')
        return False
    print('You have successfully logged in!')
    return logged_menu()


def logged_menu():
    while True:
        print('1. Balance', '2. Add income', '3. Do transfer',
              '4. Close account', '5. Log out', '0. Exit', sep='\n')
        n = int(input('enter number:'))
        if n == 1:
            balance = "SELECT balance FROM card WHERE  number = '{}'".format(
                ent_card_number)
            cursor.execute(balance)
            results = cursor.fetchone()
            print('Balance:', results[0], '\n')
            continue
        elif n == 2:
            income = int(input('Enter income:'))
            inc = "UPDATE card SET balance = balance + '{}' WHERE number = '{}'".format(
                income, ent_card_number)
            cursor.execute(inc)
            conn.commit()
            balance = "SELECT balance FROM card WHERE  number = '{}'".format(
                ent_card_number)
            cursor.execute(balance)
            results = cursor.fetchone()
            print('Balance:', results[0])
            continue
        elif n == 3:
            transfer_number = input('Enter card number:')
            transfer_check = "SELECT * FROM card WHERE  number = '{}'".format(
                transfer_number)
            cursor.execute(transfer_check)
            results = cursor.fetchone()
            if luhn_algorithm_check(transfer_number) == False:
                print(
                    'Probably you made a mistake in the card number. Please try again!',
                    '\n')
                return logged_menu()
            elif results is None:
                print('Such a card does not exist', '\n')
                return logged_menu()
            elif transfer_number == ent_card_number:
                print("You can't transfer money to the same account!", '\n')
                return logged_menu()
            else:
                tr = int(input('Enter how much money you want to transfer:'))
                balance = "SELECT balance FROM card WHERE  number = '{}'".format(
                    ent_card_number)
                cursor.execute(balance)
                results = cursor.fetchone()
                balance_new = results[0] - tr
                if balance_new >= 0:
                    inc = "UPDATE card SET balance = balance - '{}' WHERE number = '{}'".format(
                        tr, ent_card_number)
                    cursor.execute(inc)
                    trans = "UPDATE card SET balance = balance + '{}' WHERE number = '{}'".format(
                        tr, transfer_number)
                    cursor.execute(trans)
                    conn.commit()
                    print('Success!')
                else:
                    print('Not enough money!')
                    continue
        elif n == 4:
            delete_acc = "DELETE FROM card WHERE number = '{}'".format(
                ent_card_number)
            cursor.execute(delete_acc)
            conn.commit()
            print('The account has been closed!')
            break
        elif n == 5:
            print('You have successfully logged out!')
            break
        elif n == 0:
            return exit('Bye!')
        else:
            print('Wrong number')
            continue


def luhn_algorithm_check(card_number):
    card = card_number
    card_check = [int(i) for i in card]
    for index, _ in enumerate(card_check):
        if index % 2 == 0:
            card_check[index] *= 2
        if card_check[index] > 9:
            card_check[index] -= 9
    check_sum = str((10 - sum(card_check) % 10) % 10)
    print(type(check_sum))
    if check_sum == '0':
        return True
    else:
        return False


def luhn_algorithm(card_number):
    card = card_number
    card_check = [int(i) for i in card]
    for index, _ in enumerate(card_check):
        if index % 2 == 0:
            card_check[index] *= 2
        if card_check[index] > 9:
            card_check[index] -= 9
    check_sum = str((10 - sum(card_check) % 10) % 10)
    return check_sum


while True:
    print('', '1. Create an account',
          '2. Log into account',
          '0. Exit', ' ', sep='\n')
    n = int(input('enter number:'))
    if n == 0:
        exit('Bye!')
    elif n == 1:
        newCard = Card()
        newCard.init_info()
    elif n == 2:
        login()
    else:
        print('Wrong number')
        continue
