import numpy as np

class Stoplight:
    def __init__(self, pos, red = False, fake = True, first = False, last = False):
        self.pos = np.array(pos)
        self.queue = set()
        self.next = None
        self.prev = None
        self.red = red
        self.fake = fake
        self.first = first
        self.last = last
        self.get_color()
        
    def step(self):
        self.red = not self.red
        self.get_color()
        
    def get_color(self):
        if self.red == True:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)
            
    def get_last(self):
        a = self
        while a.next != None:
            a = a.next
        return a
    
class Stop_list:
    
    def __init__(self, head = None):
        self.head = head
        
    def __repr__(self):
        lst = []
        self._aid_repr(self.head, lst)
        return ' '.join(lst)
    
    def _aid_repr(self, node, lst):
        if node:
            lst.append(str(node.pos))
            self._aid_repr(node.next, lst)
    
    def append(self, other):
        if self.head == None:
            self.head = other
            return
        
        a = self.head
        while a.next != None:
            a = a.next
        other.prev = a
        a.next = other