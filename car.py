from config import *
import numpy as np
import math

class Car:
    def __init__(self, next_stop = None):
        self.pos = None
        self.direction = None
        self.distance = None
        self.next = None
        self.prev = None
        self.next_stop = next_stop
        self.next_stop.queue.add(self)
        
        self.speed = 2*LAMBDA
        self.max_speed = 4*LAMBDA
        self.acceleration = 0.02*LAMBDA
        self.lookahead = self.speed * 20

        
        self.color = (255, 255, 255)
        
    def get_direction(self):
        direction_not_norm = self.next_stop.pos - self.next_stop.prev.pos
        return direction_not_norm/np.sqrt(np.sum((direction_not_norm)**2))
        
    def determine_distance(self):
        if self.next_stop.red == True:
            return min(math.dist(self.pos, self.next.pos), 
                       math.dist(self.pos, self.next_stop.pos))
        else:
            return math.dist(self.pos, self.next.pos)
    
    def step(self):
        new_distance = self.determine_distance()
        
        #kill
        if self.next_stop.last == True and new_distance < KILL_DISTANCE:
            try:
                self.prev.next = self.next_stop
            except:
                pass
            return
        
        #new stoplight
        if np.sum(np.sign(self.next_stop.pos - self.pos) + np.sign(self.direction)) == 0:
            self.next_stop.queue.remove(self)
            self.next_stop = self.next_stop.next
            self.next_stop.queue.add(self)
            self.direction = self.get_direction()

        if new_distance < self.lookahead + SAFETY_DISTANCE:
            self.speed = max(self.speed/2, 0)
        else:
            self.speed = min(self.speed+self.acceleration, self.max_speed)
            
        self.distance = new_distance
        self.lookahead = self.speed * 20
        self.pos = self.pos + (self.speed*self.direction)

class Car_list:
    
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
        
    def front_append(self, other):
        #appending the car
        if self.head == None:
            self.head = other
            self.head.next = other.next_stop.get_last()
            #initializing the other details of the car
            other.pos = other.next_stop.pos
            other.direction = other.get_direction()
            other.distance = other.determine_distance()
            return
        
        self.head.prev = other
        a = self.head
        other.next = a
        self.head = other
        #initializing the other details of the car
        other.pos = other.next_stop.pos
        other.direction = other.get_direction()
        other.distance = other.determine_distance()