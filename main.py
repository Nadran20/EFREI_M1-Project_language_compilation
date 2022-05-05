from grammar import Grammar

def dict_to_print(dico):
    result = ""
    for key, value in dico.items():
        result += f"{key} -> "
        if str(dico[key]) == "[]":
            result += "\n"
        for index, item in enumerate(value):
            for index2, _ in enumerate(item):
                result += f"{item[index2]}"
            if index == len(value)-1:
                result += f"\n"
            else:
                result += f" | "
    return result

def main():
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
    test1.get_analyse_table()
    print("La grammaire est-elle ambigue ? ")
    print("Non, elle ne l'est pas\n" if test1.ambiguity_check() else "Oui, elle l'est\n")
    print('Analyse Table :\n')
    if(test1.ambiguity_check()):
         print(test1.get_analyse_table_to_string())
    print("Reconnaissance de mots :")
    print("Le mot est reconnu" if test1.word_recognition() else "Le mot n'est pas reconnu")

if __name__ == '__main__':
    main()