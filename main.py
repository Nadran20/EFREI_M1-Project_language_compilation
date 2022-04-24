from grammar import Grammar

if __name__ == '__main__':
    test1 = Grammar("src/Grammaire1.txt")
    print(test1)
    test1.remove_left_recursive()
    print(test1)
    test1.get_first()