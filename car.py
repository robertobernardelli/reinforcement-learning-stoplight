from config import *
import numpy as np
import math
import nodes

class Car:
    def __init__(self, path):
        self.pos = path[0].pos
        self.next = None
        self.prev = None
<<<<<<< Updated upstream
        self.next_stop = next_stop
        self.next_stop.queue.add(self)
        
        self.speed = 2*LAMBDA
        self.max_speed = 4*LAMBDA
        self.acceleration = 0.02*LAMBDA
        self.lookahead = self.speed * 20

=======
        self.path = path
        self.list_index = 0 #which node of the path connects the current linked list of cars
        self.pos_index = 1 #node of the path the car is reffering to as next_node
        self.next_node = path[self.pos_index]
        self.next_node.queue.add(self)
        self.distance = self.determine_distance()
        self.direction = self.get_direction()
        self.time = 0
        self.killed = False
>>>>>>> Stashed changes
        
        self.speed = SPEED
        self.max_speed = MAX_SPEED
        self.acceleration = ACCELERATION
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
        return np.arccos(np.clip(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)), -1.0, 1.0))

    def step(self):
        self.time += 1
        new_distance = self.determine_distance()

        #kill
        if isinstance(self.next_node, nodes.FinalNode):
            try:
<<<<<<< Updated upstream
                self.prev.next = self.next_stop
            except:
                pass
            return
=======
                self.path[self.list_index].car_list.remove_last(self)
                self.list_index = self.pos_index
                if self.killed:
                    return 0
                else:
                    return self.time
            except:
                if self.killed:
                    return 0
                else:
                    self.killed = True
                    return self.time
>>>>>>> Stashed changes
        
        #new stoplight
        if self.angle_between_vectors(self.next_node.pos - self.pos, self.direction) > np.pi/2:
            self.next_node.queue.remove(self)
            self.pos_index += 1
            self.next_node = self.path[self.pos_index]
            self.next_node.queue.add(self)
            self.direction = self.get_direction()

            #if the new stoplight is a ListNode
            if isinstance(self.next_node, nodes.ListNode):
                self.path[self.list_index].car_list.remove_last(self)
                self.list_index = self.pos_index
                self.path[self.list_index].car_list.front_append(self)

        if new_distance < self.lookahead + SAFETY_DISTANCE:
            self.speed = max(self.speed/2, 0)
        else:
            self.speed = min(self.speed+self.acceleration, self.max_speed)
            
        self.distance = new_distance
        self.lookahead = self.speed * 20
        self.pos = self.pos + (self.speed*self.direction)
<<<<<<< Updated upstream

=======
        return 0 #either 0 or the total time spent on this earth
    
>>>>>>> Stashed changes
class Car_list:
    
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

    def remove_last(self, car):
        #removing the car
        if self.head == car:
            self.head = None
            self.tail = None
            return
        
        self.tail = self.tail.prev
        self.tail.next = None