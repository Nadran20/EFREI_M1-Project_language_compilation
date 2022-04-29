from grammar import Grammar

if __name__ == '__main__':
    test1 = Grammar('src/test.txt')
    print('Lecture du langage :')
    print(test1)
    test1.remove_left_recursive()
    print('Suppression de la recursivite gauche :')
    print(test1)
    print(test1.get_first())