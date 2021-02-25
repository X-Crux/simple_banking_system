import sys
from random import randint
import sqlite3


def creat_card():
    num_generate = '400000' + ''.join(
        [str(randint(0, 9)) for _ in range(0, 9)]
    )
    card_number = algorithm_luhn(num_generate)
    card_pin = ''.join([str(randint(0, 9)) for _ in range(0, 4)])
    all_numbers = get_numbers()
    if card_number not in all_numbers:
        cur.execute(
            f'INSERT INTO card (number, pin)'
            f'VALUES ("{card_number}", "{card_pin}")'
        )
        conn.commit()
        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}\n'
              f'Your card PIN:\n{card_pin}\n')
    else:
        creat_card()


def algorithm_luhn(_number):
    step_one = [int(i) for i in list(_number)]
    step_two = []
    for i in range(0, len(step_one)):
        if (i + 1) % 2 != 0:
            step_two.append(step_one[i] * 2)
        else:
            step_two.append(step_one[i])
    step_three = []
    for i in step_two:
        if i > 9:
            step_three.append(i - 9)
        else:
            step_three.append(i)
    control_sum = str(10 - sum(step_three) % 10)
    if control_sum == '10':
        control_sum = '0'
    card_number = _number + control_sum
    return card_number


def log_in():
    card_number = str(input('\nEnter your card number:\n'))
    card_pin = str(input('Enter your PIN:\n'))
    try:
        get_pin = [i for i in cur.execute(
            f'SELECT pin FROM card WHERE number={card_number}'
        )][0][0]
        if get_pin == card_pin:
            log_info(card_number)
        else:
            print('\nWrong card number or PIN!\n')
    except Exception:
        print('\nWrong card number or PIN!\n')


def log_info(_number):
    print('\nYou have successfully logged in!')
    choice = ''
    while choice != '0':
        print(
            '\n1. Balance'
            '\n2. Add income'
            '\n3. Do transfer'
            '\n4. Close account'
            '\n5. Log out'
            '\n0. Exit'
        )
        choice = str(input())
        if choice == '1':
            print(f'\nBalance: {get_balance(_number)}')
        elif choice == '2':
            add_income(_number)
        elif choice == '3':
            do_transfer(_number)
        elif choice == '4':
            cur.execute(f'DELETE FROM card WHERE number={_number}')
            conn.commit()
            print('\nThe account has been closed!\n')
            break
        elif choice == '5':
            print('\nYou have successfully logged out!\n')
            break
        elif choice == '0':
            print('\nBye!')
            conn.close()
            sys.exit(0)
        else:
            print('\nWrong menu number!\n')


def add_income(_number):
    money_value = int(input('\nEnter income:\n'))
    _balance = get_balance(_number)
    cur.execute(
        f'UPDATE card '
        f'SET balance={_balance + money_value} '
        f'WHERE number={_number}'
    )
    conn.commit()
    print('Income was added!')


def do_transfer(_number):
    number_to_transfer = str(input('\nTransfer\nEnter card number:\n'))
    _validation = number_validation(_number, number_to_transfer)
    if _validation:
        print(_validation)
    else:
        money_value = abs(int(input(
            'Enter how much money you want to transfer:\n'
        )))
        from_balance = get_balance(_number)
        to_balance = get_balance(number_to_transfer)
        if money_value <= from_balance:
            cur.execute(
                f'UPDATE card '
                f'SET balance={from_balance - money_value} '
                f'WHERE number={_number}'
            )
            cur.execute(
                f'UPDATE card '
                f'SET balance={to_balance + money_value} '
                f'WHERE number={number_to_transfer}'
            )
            conn.commit()
            print('Success!')
        else:
            print('Not enough money!')


def number_validation(_number, number_to_transfer):
    if _number == number_to_transfer:
        return "You can't transfer money to the same account!"
    elif number_to_transfer != algorithm_luhn(number_to_transfer[:-1]):
        return "Probably you made a mistake in the card number. " \
               "Please try again!"
    elif number_to_transfer not in get_numbers():
        return "Such a card does not exist."
    else:
        return False


def get_balance(_number):
    return [i for i in cur.execute(
        f'SELECT balance FROM card WHERE number={_number}'
    )][0][0]


def get_numbers():
    return [''.join(i) for i in cur.execute('SELECT number FROM card')]


def start_menu():
    while True:
        print('1. Create an account\n2. Log into account\n0. Exit')
        choice = str(input())
        if choice == '1':
            creat_card()
        elif choice == '2':
            log_in()
        elif choice == '0':
            print('\nBye!')
            conn.close()
            sys.exit(0)
        else:
            print('\nWrong menu number!\n')


if __name__ == '__main__':
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS card ("
                "id INTEGER PRIMARY KEY,"
                "number TEXT,"
                "pin TEXT,"
                "balance INTEGER DEFAULT 0"
                ")")
    conn.commit()
    start_menu()
    conn.close()
