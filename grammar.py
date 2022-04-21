class Grammar:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.regle = {}
            lines = file.read().splitlines()
            for line in lines:
                line = line.split("->")
                line[0] = line[0].strip()
                line[1] = line[1].strip()
                line[1] = line[1].split("|")
                for index, item in enumerate(line[1]):
                    line[1][index] = item.strip()
                self.regle[line[0]] = list(set(line[1]))

    def __str__(self):
        result = ""
        for key, values in self.regle.items():
            result += f"{key} ->"
            for index, item in enumerate(values):
                if index == len(values) - 1:
                    result += f" {item}\n"
                else:
                    result += f" {item} |"
        return result

    def remove_left_recursive(self):
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup = []
            for item in values:
                if item.startswith(key):
                    recursive = True
                    sup.append(item)
                    try:
                        temp[f'{key}\''].append(f'{item[len(key):]}{key}\'')
                    except KeyError:
                        temp[f'{key}\''] = ([f'{item[len(key):]}{key}\''])
            for index, item in enumerate(values):
                if recursive == True and not item.startswith(key):
                    values[index] += f'{key}\''
            recursive = False
            for item in sup:
                values.remove(item)
                if len(self.regle[key]) == 0:
                    values.append(f"{key}\'")
        for _, values in temp.items():
            values.append("eps")
            values = list(set(values))
        self.regle = dict(self.regle, **temp)

    def get_first(self):
        first = {i: set() for i in self.regle.keys()}
        # nT : non terminal
        for nT, r in self.regle.items():
            for rules in r:
                self.calculPremier(first, nT, rules)

    def calculPremier(self, first, nT, rules):
        if rules is None:
            pass
        else:
            #print(rules)
            # si premier élément est une MAJ alors nT
            if isinstance(rules, list):
                for rule in rules:
                    self.calculPremier(first, nT, rule)
            else:
                if rules == "eps":
                    first.update({nT: rules})
                else:
                    if rules.startswith(rules[0].upper()):
                        #rules[0].upper()
                        # appelerPremier avec le premier nT
                        self.calculPremier(first, rules[0], self.regle.get(rules[0]))
                    else:
                        first.update({nT: rules[0]}) #Changer l'update pour que tout puisse etre ajouter et pas ecraser
                    print(f"ma liste {first}")
