class Grammar:

    def __init__(self, path):
        # Read only
        with open(path, 'r') as file:
            # Tableau qui stock grammaire
            self.regle = []
            lines = file.read().splitlines()
            for line in lines:
                temp = line.split('->')
                self.regle.append([temp[0]])
                temp = temp[1].split('|')
                self.regle[len(self.regle) - 1].extend(temp)

    def __str__(self):
        result = ""
        for line in self.regle:
            for index, item in enumerate(line):
                if index == 0 and len(line) > 1:
                    result += f"{item} -> "
                elif index == len(line) - 1 or index == 0:
                    result += f"{item}"
                else:
                    result += f"{item} | "
            result += "\n"
        return result

    def remove_recursive(self):
        for indexLine, line in enumerate(self.regle):
            for indexItem, item in enumerate(line[1:]):
                if (item[0] == line[0]):
                    self.regle.append([f"{line[0]}'"])
                    self.regle[len(self.regle)-1].extend([f"{item[1:]}{line[0]}'"])
                    self.regle[len(self.regle)-1].extend(['eps'])
                    del self.regle[indexLine][indexItem+1]
                    self.regle[indexLine][1] += f"{line[0]}'"
        print(self.regle)

    # def read_setence(self, setence):
