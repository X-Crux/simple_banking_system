import sys
from random import randint


def creat_card():
    card_number = algorithm_luhn()
    card_pin = str(randint(10000, 19999))[1:]
    if card_number not in db.keys():
        db[card_number] = [card_pin, 0]
        print('\nYour card has been created')
        print(f'Your card number:\n{card_number}\n'
              f'Your card PIN:\n{card_pin}\n')
    else:
        creat_card()


def algorithm_luhn():
    step_one = '400000' + str(randint(1000000000, 1999999999))[1:]
    step_one_list = [int(i) for i in list(step_one)]
    step_two = []
    for i in range(0, len(step_one_list)):
        if (i + 1) % 2 != 0:
            step_two.append(step_one_list[i] * 2)
        else:
            step_two.append(step_one_list[i])
    step_three = []
    for i in step_two:
        if i > 9:
            step_three.append(i - 9)
        else:
            step_three.append(i)
    control_sum = str(10 - sum(step_three) % 10)
    if control_sum == '10':
        control_sum = '0'
    card_number = step_one + control_sum
    return card_number


def log_in():
    card_number = str(input('\nEnter your card number:\n'))
    card_pin = str(input('Enter your PIN:\n'))
    try:
        if db[card_number][0] == card_pin:
            log_info(db[card_number][1])
        else:
            print('\nWrong card number or PIN!\n')
    except Exception:
        print('\nWrong card number or PIN!\n')


def log_info(balance):
    print('\nYou have successfully logged in!\n')
    choice = ''
    while choice != '0':
        print('1. Balance\n2. Log out\n0. Exit')
        choice = str(input())
        if choice == '1':
            print(f'\nBalance: {balance}\n')
        elif choice == '2':
            print('\nYou have successfully logged out!\n')
            break
        elif choice == '0':
            print('\nBye!')
            sys.exit(0)
        else:
            print('\nWrong menu number!\n')


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
            sys.exit(0)
        else:
            print('\nWrong menu number!\n')


if __name__ == '__main__':
    db = {}
    start_menu()
