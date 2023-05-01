import pygame
import random
import math
import numpy as np
from car import *
from nodes import *
import graph
from config import *
import networkx as nx


class Node:
    """
    Base class for all nodes
    """

    def __init__(self, id):
        self.id = id
        self.car_queue = []


class WaitingNode(Node):
    """
    Node that has a stoplight, where cars wait until the light turns green.
    Unlimited capacity for cars.
    Pedestrians will spawn here and wait if the stoplight is green (it is relative to the cars).
    """

    def __init__(self, id, stoplight):
        super().__init__(id)
        self.stoplight = stoplight
        self.pedestrian_queue = []

    def __repr__(self):
        return f"WaitingNode{self.id}\nStoplight: {self.stoplight}\nCars: {len(self.car_queue)}\nPedestrians: {len(self.pedestrian_queue)}"


class TransitionNode(Node):
    """
    Transition node, between waiting nodes and ending nodes.
    We need this because we can't have a car go from a waiting
    node to an ending node directly (we want to simulate intersection occupancy)
    Limited capacity.
    """

    def __init__(self, id, max_capacity=2):
        super().__init__(id)
        self.max_capacity = max_capacity

    def __repr__(self):
        return f"TransitionNode{self.id}\nCars: {len(self.car_queue)}"


class EndingNode(Node):
    """
    Ending node, where cars are removed from the simulation, and their wait time is recorded
    """

    def __init__(self, id):
        super().__init__(id)

    def __repr__(self):
        return f"EndingNode{self.id}"


class Entity:
    """
    Base class for all entities
    """

    def __init__(self, id, spawn_time):
        self.id = id
        self.spawn_time = spawn_time
        self.waited_time = None

    def kill(self, kill_time):
        self.waited_time = kill_time - self.spawn_time
        return self.waited_time


class Car(Entity):
    """
    Car entity
    """

    def __init__(self, id, spawn_time):
        super().__init__(id, spawn_time)

    def __repr__(self):
        return f"Car {self.id}"


class Pedestrian(Entity):
    """
    Pedestrian entity
    """

    def __init__(self, id, spawn_time):
        super().__init__(id, spawn_time)

    def __repr__(self):
        return f"Pedestrian {self.id}"


class Intersection:
    """
    Master class for the whole environment
    """

    def __init__(self):
        self.stop_lists = graph.stoplights_list.copy()
        self.car_lists = graph.car_list.copy()
        self.average_time = 0

<<<<<<< Updated upstream
        # Configuration (could be loaded from a file)
        A = WaitingNode(0, stoplight="red")
        B = WaitingNode(1, stoplight="green")
        C = TransitionNode(2)
        D = EndingNode(3)

        self.waiting_nodes = [A, B]
        self.transition_nodes = [C]

        self.G = nx.DiGraph()
        self.G.add_node(A, pos=(0, 0))
        self.G.add_node(B, pos=(1, 1))
        self.G.add_node(C, pos=(0, 1))
        self.G.add_node(D, pos=(0, 2))

        self.G.add_edge(A, C)
        self.G.add_edge(B, C)
        self.G.add_edge(C, D)

    def render(self):
        plt.close()
        fig = plt.figure()
        fig.add_subplot(111)
        edges = self.G.edges()
        colors = [
            "g"
            if (type(edge[0]) is WaitingNode and edge[0].stoplight == "green")
            or type(edge[0]) is TransitionNode
            else "r"
            for edge in edges
        ]

        pos = nx.get_node_attributes(self.G, "pos")
=======
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
>>>>>>> Stashed changes

        pos_nodes = nudge(pos, 0.08, -0.08)

        # plt.figure(1,figsize=(4,4))
        nx.draw(
            self.G, pos=pos, edge_color=colors, with_labels=False, linewidths=3, width=3
        )
        nx.draw_networkx_labels(
            self.G,
            pos=pos_nodes,
            font_size=7,
            horizontalalignment="left",
            verticalalignment="top",
        )

        # add a time step label
        avg_car_waiting_time = round(
            np.mean(
                [
                    car.waited_time
                    for car in self.all_spawned_cars
                    if car.waited_time is not None
                ]
            ),
            1,
        )
        avg_ped_waiting_time = round(
            np.mean(
                [
                    pedestrian.waited_time
                    for pedestrian in self.all_spawned_pedestrians
                    if pedestrian.waited_time is not None
                ]
            ),
            1,
        )
        label = f"Run stats:\nTime step: {self.time_step}\nAVG car waiting time: {avg_car_waiting_time}\nAVG ped. waiting time: {avg_ped_waiting_time}"
        plt.text(
            1, 0, label, horizontalalignment="left", verticalalignment="top", fontsize=7
        )

<<<<<<< Updated upstream
        ax = plt.gca()
        ax.set_xlim([-0.5, 2])
        ax.set_ylim([-0.5, 2.5])
=======
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
>>>>>>> Stashed changes

        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # invert R and B channels
        data = data[..., ::-1]

<<<<<<< Updated upstream
        cv2.imshow("test", data)
        cv2.waitKey(1)

    def switch_stoplights(self):
        for node in self.waiting_nodes:
            if node.stoplight == "green":
                node.stoplight = "red"
            else:
                node.stoplight = "green"

    def step(self):
        """
        ...
        """

        for node in self.transition_nodes:
            # kill the first car in the list
            if len(node.car_queue) > 0:
                car = node.car_queue.pop(0)
                car.kill(self.time_step)

        for node in self.waiting_nodes:
            # new pedestrians spawn
            p = np.random.uniform()
            if p < 0.1:
                # spawn a new pedestrian
                id = len(self.all_spawned_pedestrians)
                new_pedestrian = Pedestrian(id, self.time_step)
                node.pedestrian_queue.append(new_pedestrian)
                self.all_spawned_pedestrians.append(new_pedestrian)

            # new cars spawn
            p = np.random.uniform()
            if p < 0.1:
                # spawn a new car
                id = len(self.all_spawned_cars)
                new_car = Car(id, self.time_step)
                node.car_queue.append(new_car)
                self.all_spawned_cars.append(new_car)

            # pedestrian transitions (actually we kill them)
            if node.stoplight == "red":
                # pedestrians can cross
                for pedetrian in node.pedestrian_queue:
                    node.pedestrian_queue.remove(pedetrian)
                    pedetrian.kill(self.time_step)
            else:
                # move the first car to the transition node, but only if
                # the transition node is not at max capacity
                transition_node = list(self.G.successors(node))[0]
                if (
                    len(node.car_queue) > 0
                    and len(transition_node.car_queue) <= transition_node.max_capacity
                ):
                    car = node.car_queue.pop(0)
                    transition_node.car_queue.append(car)

        self.time_step += 1
=======
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
>>>>>>> Stashed changes
