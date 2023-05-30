import random
import math
import numpy as np
from car import *
from nodes import *
from graph import stoplights_list, nodes_with_list, rendering_list, starting_points, ending_points, G
from config import *
import networkx as nx
from copy import deepcopy

class Environment:
    def __init__(self):
        self.nodes_with_list = nodes_with_list.copy()
        self.stop_lists = stoplights_list.copy()
        self.graph = G.copy()
        self.average_time = []
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False
        self.kill_count = 0.0000000001
        self.cars = []

    def restart(self):
        self.flush()
        self.average_time = []
        self.screen = None
        self.background_image = None
        self.font = None
        self.is_render = False
        if self.is_render:
            pygame.display.quit()
        self.kill_count = 0.0000000001

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

        for node in rendering_list:
            pygame.draw.circle(self.screen, (0, 0, 0), node.pos, 6)

        #updating car positions
        for car in self.cars:
            pygame.draw.circle(self.screen, car.color, car.pos, 4)

        pygame.display.update()

    def step(self, switch_stoplights = False, create_car = False, speed = None, max_speed = None, acceleration = None, lookahead = None):
        
        if switch_stoplights:
            for stoplight in self.stop_lists:
                #updating stoplights
                stoplight.step()

        #cars enter the system
        if create_car:
            #get the shortest path between entrance and exit
            shortest_path = nx.shortest_path(self.graph,starting_points[0], ending_points[0])

            #append a car at the entrance list with the shortest path
            new_car = Car(shortest_path, speed, max_speed, acceleration, lookahead)
            self.cars.append(new_car)
            shortest_path[0].car_list.front_append(new_car)

        for car in self.cars:
            time = car.step()
            if time != 0:
                self.average_time.append(time)
                self.cars.remove(car)