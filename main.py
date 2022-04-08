from grammar import Grammar

if __name__ == '__main__':
    test1 = Grammar("src/test.txt")
    print(test1)
    test1.remove_left_recursive()
    print(test1)
