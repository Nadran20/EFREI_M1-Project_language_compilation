# Definition of a stack class
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def push(self, item):
        self.items.append(item)
    
    def top(self):
        return self.items[-1]

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def __str__(self) -> str:
        return str(self.items)
    