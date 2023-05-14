from config import *
import numpy as np
import math
import nodes

class Car:
    def __init__(self, path, id):
        self.id = id
        self.pos = path[0].pos
        self.next = None
        self.prev = None
        self.path = path
        self.list_index = 0 #which node of the path connects the current linked list of cars
        self.pos_index = 1 #node of the path the car is referring to as next_node
        self.next_node = path[self.pos_index]
        self.next_node.queue.add(self)
        self.distance = self.determine_distance()
        self.direction = self.get_direction()
        self.time = 0
        
        #we assume that the speed of the car is normally distributed and has 5% standard deviation
        self.speed = np.random.normal(SPEED, SPEED/20) 
        self.max_speed = np.random.normal(MAX_SPEED, MAX_SPEED/20)
        self.acceleration = np.random.normal(ACCELERATION, ACCELERATION/20)
        self.lookahead = self.speed * LOOKAHEAD
    
        self.color = (255, 255, 255)

    def determine_distance(self):
        if (isinstance(self.next_node, nodes.Stoplight) and self.next_node.red) or \
            (isinstance(self.next_node, nodes.YieldNode) and self.next_node.is_occupied()):
            if self.next == None:
                return math.dist(self.pos, self.next_node.pos)
            else:
                return min(math.dist(self.pos, self.next.pos), 
                        math.dist(self.pos, self.next_node.pos))
        elif self.next == None:
            return np.inf
        else:
            return math.dist(self.pos, self.next.pos)
        
    def get_direction(self):
        direction_not_norm = self.next_node.pos - self.pos
        return direction_not_norm/np.sqrt(np.sum((direction_not_norm)**2))
        
    def angle_between_vectors(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def step(self):
        self.time += 1
        new_distance = self.determine_distance()
        
        #new stoplight
        if self.angle_between_vectors(self.next_node.pos - self.pos, self.direction) < 0.7:
            self.next_node.queue.remove(self)
            self.pos_index += 1
            self.next_node = self.path[self.pos_index]
            self.next_node.queue.add(self)
            self.direction = self.get_direction()

            #if the new stoplight is a ListNode
            if isinstance(self.next_node, nodes.ListNode):
                self.path[self.list_index].car_list.remove_car(self)
                self.list_index = self.pos_index
                self.path[self.list_index].car_list.front_append(self)

        #kill
        if isinstance(self.next_node, nodes.FinalNode):
            self.path[self.list_index].car_list.remove_car(self)
            self.list_index = self.pos_index
            return self.time

        if new_distance < self.lookahead + SAFETY_DISTANCE:
            self.speed = max(self.speed/2, 0)
        else:
            self.speed = min(self.speed+self.acceleration, self.max_speed)
            
        self.distance = new_distance
        self.lookahead = self.speed * LOOKAHEAD
        self.pos = self.pos + (self.speed*self.direction)
        return 0 #either 0 or the total time spent on this earth
