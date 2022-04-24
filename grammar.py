
class Grammar:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.regle = {}
            self.terminaux = []
            lines=file.read().splitlines()
            for line in lines:
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
                            if(line[1][index][index2] not in self.terminaux):
                                self.terminaux.append(line[1][index][index2])
                    else:
                        line[1][index] = [['eps']]
                        if ['esp'] not in self.terminaux:
                            self.terminaux.append(['eps'])
                try :
                    self.regle[line[0]] += line[1]
                except KeyError:
                    self.regle[line[0]] = line[1]
            self.non_terminaux = [[key] for key, _ in self.regle.items()]
            for item in self.non_terminaux:
                if item in self.terminaux:
                    self.terminaux.remove(item)

    def __str__(self):
        print (f"Nous sommes les terminaux{self.terminaux}")
        print (f"Nous sommes les non-terminaux{self.non_terminaux}")
        result = ""
        for key, values in self.regle.items():
            result += f"{key} -> "
            for index, item in enumerate(values):
                for index2, _ in enumerate(item):
                    result += f"{item[index2][0]}"
                if index == len(values)-1:
                    result += f"\n"
                else:
                    result += f" | "
        return result

    def remove_left_recursive(self):
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup=[]
            for item in values:
                if item[0] == [key]:
                    recursive = True
                    sup.append(item)
                    new_item = item[1:]
                    new_item.append([f'{key}\''])
                    try:
                        temp[f'{key}\''].append(new_item)
                    except KeyError:
                        temp[f'{key}\''] = ([new_item])
            for index, item in enumerate(values): 
                if recursive==True and not item[0] == [key] :
                    values[index].append([f'{key}\''])
            recursive = False
            for item in sup:
                values.remove(item)
                if len(self.regle[key]) == 0:
                    values.append([[f"{key}\'"]])
        for _, values in temp.items():
            values.append([["eps"]])
        self.regle = dict(self.regle, **temp)
        self.non_terminaux = [[key] for key, _ in self.regle.items()]

    def get_first(self):
        first = {i: [] for i in self.regle.keys()}
        for nT, r in self.regle.items():
            for rules in r:
                print(f"regles en cours {r}")
                self.calcul_premier(first, nT, rules)

    def calcul_premier(self, first, nt, rules):
        if rules[0] in self.terminaux:
            first[nt] = [first[nt], rules[0]]
            print(f"Ajouter terminal {rules[0]} dans {nt}")
        elif rules[0] in self.non_terminaux:
            print(f"Règle avec nT {nt} {rules[0]}")
            first[nt] = [first[nt], self.calcul_nt_premier(first, nt, rules)]
        print(f"Premier :{first}")

   # si son premier c'est un nt on va chercher les premiers du nt
    def calcul_nt_premier(self, first, nt, rules):

        for i in range(len(self.non_terminaux)):
            if self.non_terminaux[i] == rules[0]:
                temp = str((self.non_terminaux[i]))
                temp = str(temp)
                print(f"{temp} valeur du non terminal, nT en cours {nt}")
        #self.calcul_Premier(first, )
        print(f"J'ai un problème de premier {nt}")
        print(f"mon toit, mes règles {rules[0]}")