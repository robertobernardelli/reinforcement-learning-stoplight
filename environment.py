import pygame
import random
import math
import numpy as np
from car import *
from stoplight import *
import roads
from config import *

class Environment:
    def __init__(self):
        self.stop_lists = roads.stl.copy()
        self.car_lists = roads.cal.copy()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None

    def restart(self):
        self.stop_lists = roads.stl.copy()
        self.car_lists = roads.cal.copy()
        self.average_time = 0
        self.screen = None
        self.background_image = None
        self.font = None

    def render(self):
        if not pygame.display.get_init():
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Traffic Simulation")

            # Load background image
            background_image = pygame.image.load("map.jpeg")
            self.background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

            # create font object
            self.font = pygame.font.SysFont('Arial', 16)   


        self.screen.blit(self.background_image, (0, 0))

        for sl, cl in zip(self.stop_lists,  self.car_lists):
            #stoplights
            stoplight = sl.head
            while stoplight != None:
                if stoplight.fake == False:
                    pygame.draw.circle(self.screen, stoplight.color, stoplight.pos, 8)
                    # render and blit number beside stoplight
                    text = self.font.render(str(len(stoplight.queue)), True, (0, 0, 0))
                    self.screen.blit(text, (stoplight.pos[0]+10, stoplight.pos[1]-10))
                stoplight = stoplight.next
        
            #cars
            if cl.head != None:
                car = cl.head
                while car.next != None:
                    pygame.draw.circle(self.screen, car.color, car.pos, 4)
                    car = car.next

        pygame.display.update()

    def step(self, switch_stoplights = False):
  
        for sl, cl in zip(self.stop_lists,  self.car_lists):
            #stoplights
            stoplight = sl.head
            while stoplight != None:
                if switch_stoplights == True and stoplight.fake == False:
                    stoplight.step()
                stoplight = stoplight.next
        
            #cars
            if min(np.random.poisson(0.001*13), 1) == 1: #rate at which to spawn cars
                cl.front_append(Car(sl.head.next))
            if cl.head != None:
                car = cl.head
                while car.next != None:
                    self.average_time += car.step()
                    car = car.next
        
        return self.average_time