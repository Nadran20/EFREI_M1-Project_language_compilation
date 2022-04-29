from grammar import Grammar

def dict_to_print(dico):
    result = ""
    for key, value in dico.items():
        result += f"{key} -> "
        for index, item in enumerate(value):
            for index2, _ in enumerate(item):
                print(key)
                if item[index2] == None:
                    result += "\n"
                else:
                    result += f"{item[index2]}"
            if index == len(value)-1:
                result += f"\n"
            else:
                result += f" | "
    return result

if __name__ == '__main__':
    test1 = Grammar('src/test.txt')
    print('Lecture du langage :')
    print(test1)
    test1.remove_left_recursive()
    print('Suppression de la recursivite gauche :')
    print(test1)
    print('First :')
    print(dict_to_print(test1.get_first()))
    print('Follow :')
    print(dict_to_print(test1.get_follow()))