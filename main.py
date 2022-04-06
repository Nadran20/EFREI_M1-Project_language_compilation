from grammar import *


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print_hi('PyCharm')
    prout = Grammar("src/test.txt")
    print(prout)
    prout.remove_recursive()
    print(prout)
    print('Audrey pute')
