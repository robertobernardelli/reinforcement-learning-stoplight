import pygame
import random
import math
import numpy as np
from car import *
from nodes import *
from config import *
import graph
import networkx as nx

pygame.init()
screen = pygame.display.set_mode((MONITOR_WIDTH, MONITOR_HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Load background image
background_image = pygame.image.load("map.jpeg")
background_image = pygame.transform.scale(background_image, (MONITOR_WIDTH, MONITOR_HEIGHT))

# create font object
font = pygame.font.SysFont('Arial', 16)

i = 0
while i < 10000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(background_image, (0, 0))
    
    for stoplight in graph.stoplights_list:
        #updating stoplights
        if i%400 == 0:
            stoplight.step()
        pygame.draw.circle(screen, stoplight.color, stoplight.pos, 8)
        # render and blit number beside stoplight
        text = font.render(str(len(stoplight.queue)), True, (0, 0, 0))
        screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))

    for node in graph.rendering_list:
        pygame.draw.circle(screen, (0, 0, 0), node.pos, 8)
    
    #cars enter the system
    if i % 2**6 == 0:
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
                pygame.draw.circle(screen, car.color, car.pos, 4)
                car = car.next
    
    pygame.display.update()
    i += 1

pygame.quit()