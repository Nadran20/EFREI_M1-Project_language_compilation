from re import compile
from stack import Stack

class Grammar:
    def __init__(self, path) -> None:
        with open(path, 'r') as file:
            self.regle = {}
            self.terminaux = []
            lines = file.read().splitlines()

            valid_lines = []
            for line in lines:
                regex_expression = compile("[A-Z]->.+([|].+)*")
                if regex_expression.match(line):
                    valid_lines.append(line)

            for line in valid_lines:
                line = line.split("->")
                line[0] = line[0].strip()
                line[1] = line[1].strip()
                line[1] = list(set(line[1].split("|")))
                for index, item in enumerate(line[1]):
                    line[1][index] = item.strip()
                    if line[1][index] != 'eps':
                        line[1][index] = list(line[1][index])
                        for index2, _ in enumerate(line[1][index]):
                            line[1][index][index2] = list(line[1][index][index2])
                            line[1][index][index2] = line[1][index][index2][0]
                            if(line[1][index][index2] not in self.terminaux):
                                self.terminaux.append(line[1][index][index2])
                    else:
                        line[1][index] = ['eps']
                        if 'eps' not in self.terminaux:
                            self.terminaux.append('eps')
                try :
                    self.regle[line[0]] += line[1]
                except KeyError:
                    self.regle[line[0]] = line[1]
            self.non_terminaux = [key for key, _ in self.regle.items()]
            for item in self.non_terminaux:
                if item in self.terminaux:
                    self.terminaux.remove(item)
            self.terminaux.append('$')

    def __str__(self) -> str:
        print (f"Nous sommes les terminaux  {self.terminaux}")
        print (f"Nous sommes les non-terminaux  {self.non_terminaux}")
        result = ""
        for key, values in self.regle.items():
            result += f"{key} -> "
            for index, item in enumerate(values):
                for index2, _ in enumerate(item):
                    result += f"{item[index2]}"
                if index == len(values)-1:
                    result += f"\n"
                else:
                    result += f" | "
        return result

    def find_letter(self) -> str :
        letter = 'A'
        while letter in self.non_terminaux and letter != 'Z':
            letter = chr(ord(letter)+1)
        return letter


    def remove_left_recursive(self) -> None:
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup=[]
            new_key = self.find_letter()
            for item in values:
                if item[0] == key:
                    self.non_terminaux.append(new_key)
                    recursive = True
                    sup.append(item)
                    new_item = item[1:]
                    new_item.append(new_key)
                    try:
                        temp[new_key].append(new_item)
                    except KeyError:
                        temp[new_key] = ([new_item])
            for index, item in enumerate(values): 
                if recursive==True and not item == key :
                    values[index].append(new_key)
            recursive = False
            for item in sup:
                values.remove(item)
                if len(self.regle[key]) == 0:
                    values.append(new_key)
        for _, values in temp.items():
            values.append(["eps"])
        self.regle = dict(self.regle, **temp)
        if 'eps' not in self.terminaux:
            self.terminaux.append('eps')
        self.non_terminaux = [key for key, _ in self.regle.items()]

    def get_first_of_key(self, value) -> list:
        first = []
        for _, item in enumerate(value):
            for index2, item2 in enumerate(item):
                if item2 in self.non_terminaux:
                    f = self.get_first_of_key(self.regle[item2])
                    if 'eps' not in f:
                        for item3 in f:
                            if item3 not in first:
                                first.append(item3)
                        break
                    else:
                        if index2 == len(item2)-1:
                            for item3 in f:
                                if item3 not in first:
                                    first.append(item3)
                        else:
                            for item3 in f:
                                if item3 not in first:
                                    first.append(item3)
                            first.remove('eps')
                else:
                    first.append(item2)
                    break
        return first

    def get_first(self) -> dict:
        first = {}
        for key, value in self.regle.items():
            first[key] = self.get_first_of_key(value)
        self.first = first
        return first

    def get_follow_of_key(self, key) -> list:
        follow = []
        if(key == list(self.regle.keys())[0]):
            follow.append('$')

        for item in self.regle:
            for id_item2 in range(len(self.regle[item])):
                if key in self.regle[item][id_item2]:
                    id_item3 = self.regle[item][id_item2].index(key)
                    if id_item3 == len(self.regle[item][id_item2])-1:
                        if self.regle[item][id_item2][id_item3] == item:
                            break
                        else:
                            f = self.get_follow_of_key(item)
                            for x in f:
                                if x not in follow:
                                    follow.append(x)
                    else:
                        while(id_item3!=len(self.regle[item][id_item2])-1):
                            id_item3+=1
                            if not self.regle[item][id_item2][id_item3] in self.non_terminaux:
                                if self.regle[item][id_item2][id_item3] not in follow:
                                    follow.append(self.regle[item][id_item2][id_item3])
                                break
                            else:
                                f = self.get_first_of_key(self.regle[item][id_item2][id_item3])  

                                if 'eps' not in f:
                                    for x in f:
                                        if x not in follow:
                                            follow.append(x)
                                        break
                                elif 'eps' in f and id_item3 != len(self.regle[item][id_item2])-1:
                                    f.remove('eps')
                                    for k in f:
                                        if k not in follow:
                                            follow.append(k)
                                elif 'eps' in f and id_item3 == len(self.regle[item][id_item2])-1:
                                    f.remove('eps')
                                    for k in f:
                                        if k not in follow:
                                            follow.append(k)
                                    f = self.get_follow_of_key(item)
                                    for x in f:
                                        if x not in follow:
                                            follow.append(x)
        return follow


    def get_follow(self) -> dict:
        follow = {}
        for key, _ in self.regle.items():
            follow[key] = self.get_follow_of_key(key)
        self.follow = follow
        return follow


#Création de la table d'analyse M à partir de first et follow sous la forme suivante :
# M = {
#   self.non_terminal[i] : { self.terminal[j] : [...] },
# }
# En suivant les regles suivante :
# 1. Pour chaque règle A à α de la grammaire, procéder aux étapes 2 et 3.
# 2. Pour chaque terminal a dans self.first[α], ajouter A à α à M[A][a].
# 3. Si eps est dans self.first[α], ajouter A à α à M[A][b] pour chaque terminal b dans 
# self.follow[A]. Si eps est dans self.first[α] et $ est dans self.follow[A], ajouter A à α à 
# M[A,$].
# 4. Faire de chaque entrée non définie de M une erreur.
# Exemple : 
# Avec la self.regle suivante :
#  {'S' : [['a'], ['(','L',')']],
#   'L' : [['S','A']]
#   'A' : [[',','S','A'], ['eps']]
# On obtient :
# M = {
#   'S' : {'a' : ['a'], '(': ['(','L',')']},
#   'L' : {'a' : ['S','A'], '(': ['S','A']},
#   'A' : {',': [',','S','A'], ')': ['eps']}
# } 
    def get_analyse_table(self) -> dict :
        analyse_table = {}
        for key, value in self.regle.items():
            for index, item in enumerate(value):
                if item[0] in self.terminaux and item[0] != 'eps':
                    if key not in analyse_table:
                        analyse_table[key] = {}
                    if item[0] not in analyse_table[key]:
                        analyse_table[key][item[0]] = []
                    analyse_table[key][item[0]].append(item)
                elif item[0] in self.non_terminaux:
                    for item2 in self.first[item[0]]:
                        if key not in analyse_table:
                            analyse_table[key] = {}
                        if item2 not in analyse_table[key]:
                            analyse_table[key][item2] = []
                        print(f"{item=} et {item2=}")
                        analyse_table[key][item2].append(item)
                elif item[0] == 'eps':
                    for item2 in self.follow[key]:
                        if key not in analyse_table:
                            analyse_table[key] = {}
                        if item[0] not in analyse_table[key]:
                            analyse_table[key][item2] = []
                        analyse_table[key][item2].append(item)
        self.analyse_table = analyse_table
        return analyse_table


    def ambiguity_check(self) -> bool :
        for key, value in self.analyse_table.items() :
            for key2, value2 in value.items() :
                if len(value2) > 1 :
                    return False
        return True

# Affichage sous la forme : 
# max(len_str_terminaux)*" " |terminaux[0] | terminaux[1] | ... | terminaux[n]
# ---------------------------------------------------------------
# non_terminaux[0] | analyse_table[non_terminaux[0]][terminal[0]] | ... | analyse_table[non_terminaux[0]][terminal[n]]
# non_terminaux[1] | analyse_table[non_terminaux[1]][terminal[0]] | ... | analyse_table[non_terminaux[1]][terminal[n]]
# ...
# non_terminaux[m] | analyse_table[non_terminaux[m]][terminal[0]] | ... | analyse_table[non_terminaux[m]][terminal[n]]
    def get_analyse_table_to_string(self) -> str :
        result = ""
        len_str_terminaux = [len(str(terminaux)[1:-1]) for terminaux in self.terminaux]
        len_str_case = [[0 for i, _ in enumerate(self.non_terminaux)] for j, _ in enumerate(self.terminaux)] 
        for index1, non_terminaux in enumerate(self.non_terminaux) :
            for index2, terminaux in enumerate(self.terminaux) :
                try:
                    if self.analyse_table[non_terminaux][terminaux][0] == ['eps']:
                        len_str_case[index2][index1] = 3
                    else :
                        len_str_case[index2][index1] = len(self.analyse_table[non_terminaux][terminaux][0])
                except KeyError :
                    len_str_case[index2][index1] = 1
        max_len_str_case = [max(len_str_case[i]) for i in range(len(self.terminaux))]
        result += max(len_str_terminaux)* " " + " │ "
        for terminaux in self.terminaux :
            if terminaux != 'eps':
                result += str(terminaux) + " "*(max_len_str_case[self.terminaux.index(terminaux)]-len(str(terminaux))) + " | "
        result += "\n" + "─"*max(len_str_terminaux)+"─"
        for i in max_len_str_case[:-1]:
            result += "┼"+ "─"*i + "──" 
        result += "┤\n"  
        for key, value in self.analyse_table.items() :
            result += str(key) + (max(len_str_terminaux)-len(str(key)))* " " + " │ "
            for terminaux in self.terminaux :
                if terminaux != 'eps':
                    try :
                        for i in value[terminaux][0] :
                            result += str(i) 
                        if value[terminaux][0] != ['eps']:
                            result +=  " "*(max_len_str_case[self.terminaux.index(terminaux)]-len(value[terminaux][0]))
                    except KeyError :
                        result += " "*max_len_str_case[self.terminaux.index(terminaux)]
                    result += " │ "
            result += "\n"
        return result

    def word_recognition(self):
        stack = Stack()
        input_word = input("Entrez un mot : ")
        input_word = list(input_word)
        input_word.append('$')
        stack.push('$')
        stack.push(list(self.regle.keys())[0])
        while stack.top() != '$' or stack.top() != input_word[0]:
            result = ""
            result1 = ""
            for i in stack.items:
                result += "   " + str(i) 
            if len(result)>20:
                result = "... "+ result[15:]
            result+=  " "*(30 - len(result))

            for i in input_word:
                result1 += str(i) + "   "
            
            if stack.top() in self.terminaux :
                if stack.top() == 'eps' :
                    result+= " SUP eps " + " "*6
                    stack.pop()
                elif stack.top() == input_word[0] :
                    result+= " SUP " + str(input_word[0]) + " " + " "*8
                    stack.pop()
                    input_word.pop(0)
                else :
                    return False
            else :
                try:
                    temp = stack.top()
                    stack.pop()
                    result += " " + str(temp) + " -> "
                    for j in self.analyse_table[temp][input_word[0]] :
                        for i in j :
                            result += str(i)
                        for i in reversed(j):
                            stack.push(i)
                    if self.analyse_table[temp][input_word[0]][0] == ['eps']:
                        result+= " "+ " "*(6-len(self.analyse_table[temp][input_word[0]][0])) 
                    else:
                        result+= " "+ " "*(8-len(self.analyse_table[temp][input_word[0]][0])) 

                except KeyError :
                    return False
            result += " " +result1
            print(result)
            print( " ├"+"─"*(len(result)-4) +"┤")
        print("   $  " + " "*24 + "FINISH" + " "*9 + " $  ")
        return True
