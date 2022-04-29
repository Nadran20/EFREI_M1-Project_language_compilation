import re

class Grammar:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.regle = {}
            self.terminaux = []
            lines=file.read().splitlines()
            valid_lines = []
            for line in lines:
                regex_expression = re.compile(".->(.+|.+[|].+)")
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


    def __str__(self):
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



    def remove_left_recursive(self):
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup=[]
            for item in values:
                if item[0] == key:
                    recursive = True
                    sup.append(item)
                    new_item = item[1:]
                    new_item.append(f'{key}\'')
                    try:
                        temp[f'{key}\''].append(new_item)
                    except KeyError:
                        temp[f'{key}\''] = ([new_item])
            for index, item in enumerate(values): 
                if recursive==True and not item == key :
                    values[index].append(f'{key}\'')
            recursive = False
            for item in sup:
                values.remove(item)
                if len(self.regle[key]) == 0:
                    values.append([f"{key}\'"])
        for _, values in temp.items():
            values.append(["eps"])
        self.regle = dict(self.regle, **temp)
        self.non_terminaux = [key for key, _ in self.regle.items()]


    def get_first_of_key(self, key, value):
        first = []
        for item in value:
            #print(f"{item=}")
            continue
        return first

    def get_first(self):
        first = {}
        for key, value in self.regle.items():
            first[key] = self.get_first_of_key(key, value)
        return first