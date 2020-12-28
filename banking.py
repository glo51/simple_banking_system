from random import randint
from sqlite3 import connect

conn = connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card (
    id INTEGER AUTO_INCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    )''')
conn.commit()


def random_number():
    result = '400000'
    total = 0

    for x in range(9):
        result += str(randint(0, 9))
    for i, value in enumerate(result, 1):
        value = int(value)
        if i % 2 != 0:
            value = value * 2
        if value > 9:
            value = value - 9
        total += value

    for x in range(10):
        if (total + x) % 10 == 0:
            result += str(x)
            break

    cur.execute('SELECT number FROM card')
    if result not in cur.fetchall():
        return result
    else:
        random_number()


def check_luhn(to_test):
    check = 0
    total = 0
    for i, value in enumerate(to_test, 1):
        value = int(value)
        if i <= 15:
            if i % 2 != 0:
                value = value * 2
            if value > 9:
                value = value - 9
            total += value

    for x in range(10):
        if (total + x) % 10 == 0:
            check = x
            break

    if to_test[15] == str(check):
        return True
    else:
        return False


def random_pin():
    r_pin = ''
    for x in range(4):
        r_pin = r_pin + str(randint(0, 9))
    return r_pin


while True:
    print('1. Create an account\n2. Log into account\n0. Exit')
    answer = int(input())

    if answer == 0:
        break
    elif answer == 1:
        number = random_number()
        pin = random_pin()
        cur.execute(f'INSERT INTO card (number, pin) VALUES ("{number}", "{pin}")')
        conn.commit()
        print(f'\nYour card has been created\nYour card number:\n{number}\nYour card PIN:\n{pin}\n')
    elif answer == 2:
        print('\nEnter your card number:')
        number = input()
        print('Enter your PIN:')
        pin = input()

        cur.execute(f'SELECT * FROM card WHERE number="{number}" AND pin="{pin}"')
        if cur.fetchall():
            print('\nYou have successfully logged in!')
            while True:
                print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
                answer = int(input())
                if answer == 0:
                    quit()
                elif answer == 1:
                    cur.execute(f'SELECT balance FROM card WHERE number="{number}"')
                    print(f'\nBalance: {int(cur.fetchone()[0])}\n')
                elif answer == 2:
                    print('Enter income:')
                    income = int(input())
                    cur.execute(f'UPDATE card SET balance=balance+{income} WHERE number="{number}" AND pin="{pin}"')
                    conn.commit()
                    print('Income was added!\n')
                elif answer == 3:
                    print('Enter card number:')
                    destination = input()
                    cur.execute(f'SELECT * FROM card WHERE number="{destination}"')
                    if destination == number:
                        print("You can't transfer money to the same account!\n")
                    elif not check_luhn(destination):
                        print('Probably you made mistake in the card number. Please try again!\n')
                    elif not cur.fetchall():
                        print('Such a card does not exist.\n')
                    else:
                        print('Enter how much money you want to transfer:')
                        amount = int(input())
                        cur.execute(f'SELECT balance FROM card WHERE number="{number}"')
                        if amount > int(cur.fetchone()[0]):
                            print('Not enough money!\n')
                        else:
                            cur.execute(f'UPDATE card SET balance=balance-{amount} WHERE number="{number}"')
                            conn.commit()
                            cur.execute(f'UPDATE card SET balance=balance+{amount} WHERE number="{destination}"')
                            conn.commit()
                            print('Success!\n')
                elif answer == 4:
                    cur.execute(f'DELETE FROM card WHERE number="{number}" AND pin="{pin}"')
                    conn.commit()
                    print('The account has been closed!\n')
                    break
                elif answer == 5:
                    print('You have successfully logged out!\n')
                    break
                else:
                    print('\nType in the proper number\n')
        else:
            print('\nWrong card number or PIN!')
    else:
        print('\nType in the proper number\n')

conn.close()
