import pygame
import random
import math
import numpy as np
from car import *
from stoplight import *
import roads
from config import *

class environment:
    def __init__(self):
        self.stop_lists = roads.stl.copy()
        self.car_lists = roads.cal.copy()
        self.average_time = 0

    def restart(self):
        self.stop_lists = roads.stl.copy()
        self.car_lists = roads.cal.copy()
        self.average_time = 0

    def step(self, change_stoplight = False, render = False):

        if render == True:
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Traffic Simulation")

            # Load background image
            background_image = pygame.image.load("map.jpeg")
            background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

            # create font object
            font = pygame.font.SysFont('Arial', 16)    
            screen.blit(background_image, (0, 0))
            
        for sl, cl in zip(self.stop_lists,  self.car_lists):
            #stoplights
            stoplight = sl.head
            while stoplight != None:
                if change_stoplight == True and stoplight.fake == False:
                    stoplight.step()
                if render == True and stoplight.fake == False:
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
                    self.average_time += car.step()
                    if render == True:
                        pygame.draw.circle(screen, car.color, car.pos, 4)
                    car = car.next
                    
            if render == True:
                pygame.display.update()
        
        return self.average_time