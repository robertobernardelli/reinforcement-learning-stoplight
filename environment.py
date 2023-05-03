import random
import math
import numpy as np
from car import *
from nodes import *
from graph import stoplights_list, car_list, rendering_list, paths, G
from config import *
import networkx as nx
from copy import deepcopy

class Environment:
    def __init__(self):
        self.car_lists = car_list.copy()
        self.stop_lists = stoplights_list.copy()
        self.graph = G.copy()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False
        self.kill_count = 0.0000000001

    def restart(self):
        self.flush()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False
        if self.is_render:
            pygame.display.quit()
        self.kill_count = 0.0000000001

    def flush(self):
        for cl in self.car_lists:
            cl.head = None
            cl.tail = None
        
        for node in G.nodes():
            node.queue = set()

        for stoplight in self.stop_lists:
            stoplight.red = stoplight.start_red
            stoplight.get_color()
            stoplight.wait = -1

    def render(self):
        if not self.is_render:
            global pygame
            import pygame
            self.is_render = True
            
        #if not pygame.display.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
            pygame.display.set_caption("Traffic Simulation")

            # Load background image
            background_image = pygame.image.load("map.jpeg")
            self.background_image = pygame.transform.scale(background_image, (MONITOR_WIDTH, MONITOR_HEIGHT))

            # create font object
            self.font = pygame.font.SysFont('Arial', 16)   


        self.screen.blit(self.background_image, (0, 0))

        for stoplight in self.stop_lists:
            pygame.draw.circle(self.screen, stoplight.color, stoplight.pos, 8)
            # render and blit number beside stoplight
            text = self.font.render(str(len(stoplight.queue)), True, (0, 0, 0))
            self.screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))

        #updating car positions
        for cl in self.car_lists:
            if cl.tail != None:
                car = cl.tail
                while car != None:
                    pygame.draw.circle(self.screen, car.color, car.pos, 4)
                    car = car.prev

        pygame.display.update()

    def step(self, switch_stoplights = False):

        for stoplight in self.stop_lists:
            if switch_stoplights:
                if stoplight.red:
                    stoplight.wait = 5*32
                else:
                    stoplight.step()
            if stoplight.wait == 0:
                stoplight.step()
            if stoplight.wait >= 0:
                stoplight.wait -= 1

        #cars enter the system
        for path in paths:
            if min(np.random.poisson(path[2]/32), 1) == 1: #/32
                #get the shortest path between entrance and exit
                shortest_path = nx.shortest_path(G, path[0], path[1])

                #append a car at the entrance list with the shortest path
                shortest_path[0].car_list.front_append(Car(shortest_path))

        #updating car positions
        for cl in self.car_lists:
            if cl.tail != None:
                car = cl.tail
                while car != None:
                    time = car.step()
                    if time != 0:
                        self.average_time += time
                        self.kill_count += 1
                    car = car.prev
        
        return [self.average_time/self.kill_count] + [len(stoplight.queue) for stoplight in self.stop_lists]