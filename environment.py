import pygame
import random
import math
import numpy as np
from car import *
from nodes import *
import graph
from config import *
import networkx as nx

class Environment:
    def __init__(self):
        self.stop_lists = graph.stoplights_list.copy()
        self.car_lists = graph.car_list.copy()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None

    def restart(self):
        self.stop_lists = graph.stoplights_list.copy()
        self.car_lists = graph.car_list.copy()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None

    def render(self):
        if not pygame.display.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
            pygame.display.set_caption("Traffic Simulation")

            # Load background image
            background_image = pygame.image.load("map.jpeg")
            self.background_image = pygame.transform.scale(background_image, (MONITOR_WIDTH, MONITOR_HEIGHT))

            # create font object
            self.font = pygame.font.SysFont('Arial', 16)   


        self.screen.blit(self.background_image, (0, 0))

        for stoplight in graph.stoplights_list:
            pygame.draw.circle(self.screen, stoplight.color, stoplight.pos, 8)
            # render and blit number beside stoplight
            text = self.font.render(str(len(stoplight.queue)), True, (0, 0, 0))
            self.screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))

        #updating car positions
        for cl in graph.car_list:
            if cl.tail != None:
                car = cl.tail
                while car != None:
                    pygame.draw.circle(self.screen, car.color, car.pos, 4)
                    car = car.prev

        pygame.display.update()

    def step(self, switch_stoplights = False):
        
        if switch_stoplights:
            for stoplight in graph.stoplights_list:
                #updating stoplights
                stoplight.step()

        #cars enter the system
        if min(np.random.poisson(0.01*3), 1) == 1:
            #random sampling from entrances and exits (repeated if the entrance/exit is the same)
            starting_points_frequencies = np.array([x.frequency for x in graph.starting_points])
            ending_points_frequencies = np.array([x.frequency for x in graph.ending_points])

            starting_point = np.random.choice(graph.starting_points, p = starting_points_frequencies/starting_points_frequencies.sum())
            ending_point = np.random.choice(graph.ending_points, p = ending_points_frequencies/ending_points_frequencies.sum())

            while (starting_point, ending_point) in graph.forbidden_paths:
                starting_point = np.random.choice(graph.starting_points, p = starting_points_frequencies/starting_points_frequencies.sum())
                ending_point = np.random.choice(graph.ending_points, p = ending_points_frequencies/ending_points_frequencies.sum())

            #get the shortest path between entrance and exit
            shortest_path = nx.shortest_path(graph.G, starting_point, ending_point)

            #append a car at the entrance list with the shortest path
            shortest_path[0].car_list.front_append(Car(shortest_path))

        #updating car positions
        for cl in graph.car_list:
            if cl.head != None:
                car = cl.head
                while car != None:
                    car.step()
                    car = car.next
        
        return self.average_time