import re


class Grammar:
    def __init__(self, path) -> None:
        with open(path, 'r') as file:
            self.regle = {}
            self.terminaux = []
            lines = file.read().splitlines()
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
                            if line[1][index][index2] not in self.terminaux:
                                self.terminaux.append(line[1][index][index2])
                    else:
                        line[1][index] = ['eps']
                        if 'eps' not in self.terminaux:
                            self.terminaux.append('eps')
                try:
                    self.regle[line[0]] += line[1]
                except KeyError:
                    self.regle[line[0]] = line[1]
            self.non_terminaux = [key for key, _ in self.regle.items()]
            for item in self.non_terminaux:
                if item in self.terminaux:
                    self.terminaux.remove(item)

    def __str__(self) -> str:
        result = ""
        for key, values in self.regle.items():
            result += f"{key} -> "
            for index, item in enumerate(values):
                for index2, _ in enumerate(item):
                    result += f"{item[index2]}"
                if index == len(values) - 1:
                    result += f"\n"
                else:
                    result += f" | "
        return result

    def remove_left_recursive(self) -> None:
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup = []
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
                if recursive == True and not item == key:
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
                        if index2 == len(item2) - 1:
                            for item3 in f:
                                if item3 not in first:
                                    first.append(item3)

                        else:
                            for item3 in f:
                                if item3 not in first:
                                    first.append(item3)

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
        #REGLE 1
        if key == list(self.regle.keys())[0]:
            follow.append('$')

        for item in self.regle:
            for item2 in range(len(self.regle[item])):
                if key in self.regle[item][item2]:
                    idx = self.regle[item][item2].index(key)
                    if idx == len(self.regle[item][item2]) - 1:
                        if self.regle[item][item2][idx] == item:
                            break
                        else:
                            f = self.get_follow_of_key(item)
                            for x in f:
                                if x not in follow:
                                    follow.append(x)
                    else:
                        while idx != len(self.regle[item][item2]) - 1:
                            idx += 1
                            if not self.regle[item][item2][idx] in self.non_terminaux:
                                if self.regle[item][item2][idx] not in follow:
                                    follow.append(self.regle[item][item2][idx])
                                break
                            #REGLE 2 A -> aBb premier de b dans B sans eps dans S(B)
                            else:
                                f = self.first[self.regle[item][item2][idx]]

                                if 'eps' not in f:
                                    for x in f:
                                        if x not in follow:
                                            follow.append(x)
                                        break
                                elif 'eps' in f and idx != len(self.regle[item][item2]) - 1:
                                    f.remove('eps')
                                    for k in f:
                                        if k not in follow:
                                            follow.append(k)
                                elif 'eps' in f  and idx == len(self.regle[item][item2]) - 1:
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
        for key, value in self.regle.items():
            follow[key] = self.get_follow_of_key(key)
        self.follow = follow
        return follow