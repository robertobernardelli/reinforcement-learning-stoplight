import numpy as np

class Node:
    """
    Base class for a node
    """
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.queue = set()

class ListNode(Node):
    """
    This node references a linked list of cars
    """
    def __init__(self, pos):
        super().__init__(pos)
        self.car_list = None

    def append_car_list(self, car_list):
        self.car_list = car_list

class YieldNode(Node):
    """
    Its purpose is to check whether the area in front of this node is free from cars
    """
    def __init__(self, pos):
        super().__init__(pos)
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
    def __init__(self, pos, red = False):
        super().__init__(pos)
        self.red = red
        self.get_color()

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
    def __init__(self, pos, frequency = 0):
        super().__init__(pos)
        self.frequency = frequency

class FinalNode(Node):
    """
    This is where cars are killed :(
    """
    def __init__(self, pos, frequency = 0):
        super().__init__(pos)
        self.frequency = frequency