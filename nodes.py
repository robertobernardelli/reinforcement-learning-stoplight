import numpy as np

class Node:
    """
    Base class for a node
    """
    def __init__(self, pos, name = None):
        self.pos = np.array(pos)
        self.name = name
        self.queue = set()

class ListNode(Node):
    """
    This node references a linked list of cars
    """
    def __init__(self, pos, name = None):
        super().__init__(pos, name)
        self.car_list = CarList() #this class is defined below

class YieldNode(Node):
    """
    Its purpose is to check whether the area in front of this node is free from cars
    """
    def __init__(self, pos, name = None):
        super().__init__(pos, name)
        self.node_list = []

    def is_occupied(self):
        for node in self.node_list:
            if node.queue:
                return True
        return False
    
class Stoplight(YieldNode):
    """
    This node represents a stoplight
    """
    def __init__(self, pos, red = False, name = None):
        super().__init__(pos, name)
        self.start_red = red
        self.red = red
        self.get_color()
        self.wait = -1

    def step(self):
        self.red = not self.red
        self.get_color()

    def get_color(self):
        if self.red == True:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)

class InitialNode(ListNode):
    """
    We can find this node at the beginning of a road
    """
    def __init__(self, pos, name = None):
        super().__init__(pos, name)

class FinalNode(Node):
    """
    This is where cars are killed :(
    """
    def __init__(self, pos, name = None):
        super().__init__(pos, name)

class CarList:
    
    def __init__(self):
        self.head = None
        self.tail = None
        
    def __repr__(self):
        lst = []
        self._aid_repr(self.head, lst)
        return ' '.join(lst)
    
    def _aid_repr(self, node, lst):
        if node:
            lst.append(str(node.pos))
            self._aid_repr(node.next, lst)
        
    def front_append(self, car):
        #appending the car
        if self.head == None:
            self.head = car
            self.tail = car
            return

        self.head.prev = car
        car.next = self.head
        self.head = car

    def remove_car(self, car):
        #removing the car from the linked list
        if self.tail == car and self.head == car:
            self.head = None
            self.tail = None

        elif self.tail == car:
            self.tail = self.tail.prev
            self.tail.next = None
        
        elif self.head == car:
            self.head = self.head.next
            self.head.prev = None
        
        else:
            if car.next:
                if car.prev:
                    car.next.prev = car.prev
                else:
                    car.next.prev = None

            if car.prev:
                if car.next:
                    car.prev.next = car.next
                else:
                    car.prev.next = None
            
        car.prev = None
        car.next = None