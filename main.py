import pygame
import random
import math
import numpy as np
from car import *
from stoplight import *
import roads

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Load background image
background_image = pygame.image.load("map.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# create font object
font = pygame.font.SysFont('Arial', 16)

i = 0
while i < 100000:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.blit(background_image, (0, 0))
    
    for sl, cl in zip(roads.stl, roads.cal):
        #stoplights
        stoplight = sl.head
        while stoplight != None:
            if i%400 == 0 and stoplight.fake == False:
                stoplight.step()
            if stoplight.fake == False:
                pygame.draw.circle(screen, stoplight.color, stoplight.pos, 8)
                # render and blit number beside stoplight
                text = font.render(str(len(stoplight.queue)), True, (0, 0, 0))
                screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))
            stoplight = stoplight.next
    
        #cars
        if min(np.random.poisson(0.001*13), 1) == 1: #rate at which to spawn cars
            cl.front_append(Car(sl.head.next))
        if cl.head != None:
            car = cl.head
            while car.next != None:
                car.step()
                pygame.draw.circle(screen, car.color, car.pos, 4)
                car = car.next
            
    pygame.display.update()
    i += 1

pygame.quit()
