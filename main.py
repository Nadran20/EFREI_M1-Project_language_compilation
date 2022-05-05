from grammar import Grammar
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


""" 
-- fonction qui nous permet d'afficher les premiers et les suivants de nos grammaires
"""
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
    exit = False

    while not exit:
        cls()

        fichierChargé = False
        while not fichierChargé:
            print('Indiquez le nom de votre fichier de grammaire :')
            src = input()
            try:
                grammaire = Grammar(f"src/{src}")
                fichierChargé = True
            except FileNotFoundError: 
                print('Fichier Introuvable !\n')
            except Exception:
                print("Votre fichier ne contient aucune ligne correct !\nMerci de bien vouloir verifier son contenu")

        cls()
        print('Lecture du langage :')
        print(grammaire)
        print('\nSuppression de la recursivite gauche...\n')
        grammaire.remove_left_recursive()
        print('grammaire non récursive : \n')
        print(grammaire)
        print('First :')
        print(dict_to_print(grammaire.get_first()))
        print('Follow :')
        print(dict_to_print(grammaire.get_follow()))
        grammaire.get_analyse_table()
        print("La grammaire est-elle ambigue ? ")
        print("Non, elle ne l'est pas\n" if grammaire.ambiguity_check() else "Oui, elle l'est\n")
        print('Analyse Table :\n')
        if(grammaire.ambiguity_check()):
            print(grammaire.get_analyse_table_to_string())

        tryAgain = False
        while not tryAgain:
            print("Reconnaissance de mots :")
            print("Le mot est reconnu" if grammaire.word_recognition() else "Le mot n'est pas reconnu")
            print("Voulez vous reconnaitre un autre mot ? (O/N)")
            x = input()
            if x.upper() == "N":
                tryAgain = True

        print('Fin de test avec la grammaire : ' + src)
        cls()

        print("Voulez vous tester une autre grammaire ? (O/N)")
        x = input()
        if x.upper() == "N":
            exit = True


if __name__ == '__main__':
    main()