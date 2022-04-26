from grammar import Grammar

if __name__ == '__main__':
    test1 = Grammar('src/test2')
    print('Lecture du langage :')
    print(test1)
    test1.remove_left_recursive()
    print('Suppression de la récursivité gauche :')
    print(test1)


    print('Premier du langage attendu :')
    print("{'X': ['a'], ['eps'], ['b'], ['u'], 'Y' : ['a'], ['u'], ['eps'], 'Z': ['a'], ['b'], ['eps'], 'A': [['a'], ['eps']], 'B': [['u']]}" )

    print('Premier du langage obtenu :')
    print(test1.get_first())

