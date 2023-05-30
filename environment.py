import random
import math
import numpy as np
from car import *
from nodes import *
from graph import stoplights_list, nodes_with_list, rendering_list, paths, G
from config import *
import networkx as nx

class Environment:
    def __init__(self):
        #copying assets from graph.py
        self.nodes_with_list = nodes_with_list.copy()
        self.stop_lists = stoplights_list.copy()
        self.graph = G.copy()
        
        #initializing environment variables
        self.average_time = 0
        self.kill_count = 0.0000000001 #to avoid division by zero
        self.cars = []

        #rendering variables
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False

    def restart(self):
        self.flush()
        self.average_time = 0
        self.kill_count = 0.0000000001
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False
        if self.is_render:
            pygame.display.quit()
        

    #flush the environment of all cars and reset the stoplights
    def flush(self):
        self.cars = []

        for node in self.nodes_with_list:
            node.car_list.head = None
            node.car_list.tail = None
        
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
            
            pygame.init()
            self.screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
            pygame.display.set_caption("Traffic Simulation")

            # Load background image
            background_image = pygame.image.load("map.jpeg")
            self.background_image = pygame.transform.scale(background_image, (MONITOR_WIDTH, MONITOR_HEIGHT))

            # create font object
            self.font = pygame.font.SysFont('Arial', 16)   


        self.screen.blit(self.background_image, (0, 0))

        #rendering stoplights
        for stoplight in self.stop_lists:
            pygame.draw.circle(self.screen, stoplight.color, stoplight.pos, 8)
            # render and blit number beside stoplight
            text = self.font.render(str(len(stoplight.queue)), True, (0, 0, 0))
            self.screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))

        #rendering nodes if they are in the rendering list for debugging
        for node in rendering_list:
            pygame.draw.circle(self.screen, (0, 0, 0), node.pos, 6)

        #rendering cars
        for car in self.cars:
            pygame.draw.circle(self.screen, car.color, car.pos, 4)

        pygame.display.update()

    def step(self, switch_stoplights = False):

        #stoplights switch
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
                new_car = Car(shortest_path, np.random.random_integers(0, 10000000000))
                self.cars.append(new_car)
                shortest_path[0].car_list.front_append(new_car)

        #cars move
        for car in self.cars:
            time = car.step()
            if time != 0:
                self.average_time += time
                self.kill_count += 1
                self.cars.remove(car)

        #return the average waiting time and the number of cars in each stoplight queue
        return [self.average_time/self.kill_count] + [len(stoplight.queue) for stoplight in self.stop_lists]