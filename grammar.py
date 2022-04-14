class Grammar:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.regle = {}
            lines=file.read().splitlines()
            for line in lines:
                line = line.split("->")
                line[0] = line[0].strip()
                line[1] = line[1].strip()
                line[1] = line[1].split("|")
                for index, item in enumerate(line[1]):
                    line[1][index] = item.strip()
                self.regle[line[0]] = line[1]


    def __str__(self):
        result = ""
        for key, values in self.regle.items():
            result += f"{key} ->"
            for index, item in enumerate(values):
                if (index == len(values)-1):
                    result += f" {item}\n"
                else:
                    result += f" {item} |"
        return result


    def remove_left_recursive(self):
        recursive = False
        temp = {}
        for key, values in self.regle.items():
            sup=[]
            for index, item in enumerate(values):
                if item.startswith(key):
                    recursive = True
                    sup.append(item)
                    try:
                        temp[f'{key}\''].append(f'{item[len(key):]}{key}\'')
                    except KeyError:
                        temp[f'{key}\''] = ([f'{item[len(key):]}{key}\''])
                if recursive==True and not item.startswith(key):
                    values[index]+=f'{key}\''
            recursive=False
            for item in sup:
                values.remove(item)
                if len(self.regle[key]) == 0:
                    values.append(f"{key}\'") 
        for key, values in temp.items():
            values.append("eps")
        self.regle = dict (self.regle, **temp)
