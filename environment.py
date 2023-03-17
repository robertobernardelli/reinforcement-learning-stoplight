import networkx as nx
from utils import *
import matplotlib.pyplot as plt
import numpy as np


class Node:
    """
    Base class for all nodes
    """

    def __init__(self, id):
        self.id = id
        self.car_queue = []
        self.stop = False # This is used to stop the cars at the node


class StoplightNode(Node):
    """
    Node that has a stoplight, where cars wait until the light turns green.
    Unlimited capacity for cars.
    Pedestrians will spawn here and wait if the stoplight is green (it is relative to the cars).
    """

    def __init__(self, id, stoplight):
        super().__init__(id)
        self.stoplight = stoplight
        self.pedestrian_queue = []
        
    def update(self):
        """
        If the stoplight is green, we let the cars go. 
        We also check that the car_queue of the next node is not full.
        """
        if self.stoplight == "green":
            self.stop = False
        else:
            self.stop = True

    def __repr__(self):
        return f"StoplightNode{self.id}\nStoplight: {self.stoplight}\nCars: {len(self.car_queue)}\nPedestrians: {len(self.pedestrian_queue)}"


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
    
    def update(self):
        """
        In our scenario, transition nodes are always open.
        """
        self.stop = False

    def __repr__(self):
        return f"TransitionNode{self.id}\nCars: {len(self.car_queue)}"

class YieldNode(TransitionNode):
    """
    Special case of Transition node, between two Transition Nodes.
    We need this when we want to simulate a car stopping in the middle of the intersection
    for the right of way.
    Limited capacity.
    """

    def __init__(self, id, yield_to, max_capacity=2):
        super().__init__(id, max_capacity)
        self.yield_to = yield_to
    
    def update(self):
        """
        For Yield nodes, we check if the self.yield_to has cars in it.
        """
        if len(self.yield_to.car_queue) > 0:
            self.stop = True
        else:
            self.stop = False

    def __repr__(self):
        return f"YieldNode{self.id}\nCars: {len(self.car_queue)}"

class EndingNode(Node):
    """
    Ending node, where cars are removed from the simulation, and their wait time is recorded
    """

    def __init__(self, id):
        super().__init__(id)
        
    def update(self):
        # we don't need to do anything here
        self.stop = False

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

    def __init__(self, id, spawn_time, trajectory):
        super().__init__(id, spawn_time)
        self.trajectory = trajectory
        self.distance_traveled = 0
        self.current_node = self.trajectory.path[0]
        self.current_speed = 0
        self.acceleration = 0.1
        self.max_speed = 8
        
        self.cool_down = 0 # how many steps before initiating transition to next node (to simulate transition time longer than 1 timestep)
        
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

class Trajectory:
    """
    Helper class to store a trajectory. Every car has a trajectory.
    """
    def __init__(self, id, path, lenght=100):
        self.id = id
        self.path = path    # list of nodes
        self.lenght = lenght
    
    def __repr__(self):
        return f"Trajectory {self.id}"

class Intersection:
    """
    Master class for the whole environment
    """

    def __init__(self):
        # Parameters
        self.time_step = 0
        # keep track of all spawned cars and pedestrians:
        self.all_spawned_cars = []
        self.all_spawned_pedestrians = []

        # Configuration (could be loaded from a file)
        A = StoplightNode('A', stoplight="green")
        B = TransitionNode('B')
        C = TransitionNode('C')
        D = EndingNode('D')
        E = EndingNode('E')
        
        G = TransitionNode('G')
        H = EndingNode('H')
        
        I = StoplightNode('I', stoplight="green")
        K = TransitionNode('K')
        L = EndingNode('L')
        
        M = StoplightNode('M', stoplight="red")
        O = StoplightNode('O', stoplight="red")
        
        
        F = YieldNode('F', yield_to=G)
        P = YieldNode('P', yield_to=K)
        J = YieldNode('J', yield_to=B)
        N = YieldNode('N', yield_to=C)

        self.G = nx.DiGraph()
        
        self.G.add_node(A, pos=(0.3, 0))
        self.G.add_node(B, pos=(0.3, 0.1))
        self.G.add_node(C, pos=(0.3, 0.2))
        self.G.add_node(D, pos=(0.3, 0.3))
        self.G.add_node(E, pos=(0.4, 0.1))
        self.G.add_node(F, pos=(0.28, 0.18))
        self.G.add_node(G, pos=(0.2, 0.2))
        self.G.add_node(H, pos=(0.1, 0.2))
        
        self.G.add_node(I, pos=(0.2, 0.3))
        self.G.add_node(J, pos=(0.22, 0.12))
        self.G.add_node(K, pos=(0.2, 0.1))
        self.G.add_node(L, pos=(0.2, 0))
        
        self.G.add_node(M, pos=(0.1, 0.1))
        self.G.add_node(N, pos=(0.28, 0.12))
        
        self.G.add_node(O, pos=(0.4, 0.2))
        self.G.add_node(P, pos=(0.22, 0.18))
        

        self.G.add_edge(A, B)
        self.G.add_edge(B, C)
        self.G.add_edge(C, D)
        self.G.add_edge(B, E)
        self.G.add_edge(B, F)
        self.G.add_edge(F, G)
        self.G.add_edge(G, H)
        
        self.G.add_edge(I, G)
        self.G.add_edge(G, J)
        self.G.add_edge(J, B)
        self.G.add_edge(G, K)
        self.G.add_edge(K, L)
        
        self.G.add_edge(M, K)
        self.G.add_edge(K, N)
        self.G.add_edge(N, C)
        
        self.G.add_edge(O, C)
        self.G.add_edge(C, P)
        self.G.add_edge(P, K)
        
        self.G.add_edge(K, B)
        self.G.add_edge(C, G)
    
        
        self.stoplight_nodes = [A, I, M, O]
        self.transition_nodes = [B, C, F, G, J, K, N, P]
        self.ending_nodes = [D, E, H, L]
        self.yield_nodes = [F, P, J, N]
        
        t1 = Trajectory(1, [A, B, C, D])
        t2 = Trajectory(2, [A, B, N])
        t3 = Trajectory(3, [A, B, F, G, H])
        
        t4 = Trajectory(4, [I, G, K, L])
        t5 = Trajectory(5, [I, G, H])
        t6 = Trajectory(6, [I, G, J, B, N])
        
        t7 = Trajectory(7, [M, K, B, N])
        t8 = Trajectory(8, [M, K, L])
        t9 = Trajectory(9, [M, K, N, C, D])
        
        t10 = Trajectory(10, [O, C, G, H])
        t11 = Trajectory(11, [O, C, D])
        t12 = Trajectory(11, [O, C, P, K, L])
        
        self.trajectories = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]
        

    def render(self):
        plt.close()
        fig = plt.figure()
        fig.add_subplot(111)
        edges = self.G.edges()
        colors = [
            "g"
            if edge[0].stop == False
            else "r"
            for edge in edges
        ]

        pos = nx.get_node_attributes(self.G, "pos")

        pos_nodes = nudge(pos, 0.01, -0.01)

        # plt.figure(1,figsize=(4,4))
        nx.draw(
            self.G, pos=pos, edge_color=colors, with_labels=False, linewidths=3, width=3
        )
        nx.draw_networkx_labels(
            self.G,
            pos=pos_nodes,
            font_size=5,
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

        ax = plt.gca()
        #ax.set_xlim([-0.01, 1.1])
        #ax.set_ylim([-0.01, 1.1])

        fig.canvas.draw()
        data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # invert R and B channels
        data = data[..., ::-1]

        cv2.imshow("render", data)
        cv2.waitKey(1)

    def switch_stoplights(self):
        for node in self.stoplight_nodes:
            if node.stoplight == "green":
                node.stoplight = "red"
            else:
                node.stoplight = "green"
    
    def spawn_some_cars(self, num_cars):
        for i in range(num_cars):
            id = len(self.all_spawned_cars)
            trajectory = np.random.choice(self.trajectories)
            new_car = Car(id, self.time_step, trajectory)
            self.stoplight_nodes[0].car_queue.append(new_car)
            self.all_spawned_cars.append(new_car)
    
    def spawn_pedestrian(self, node, prob=0.1):
        # new pedestrians spawn 
        # p is the probability of spawning a new pedestrian at each time step
        
        p = np.random.uniform()
        if p < prob:
            # spawn a new pedestrian
            id = len(self.all_spawned_pedestrians)
            new_pedestrian = Pedestrian(id, self.time_step)
            node.pedestrian_queue.append(new_pedestrian)
            self.all_spawned_pedestrians.append(new_pedestrian)
    
    def spawn_car(self, node, prob=0.1):
        # new cars spawn
        p = np.random.uniform()
        if p < prob:
            # spawn a new car
            id = len(self.all_spawned_cars)
            trajectory = np.random.choice(self.trajectories)
            new_car = Car(id, self.time_step, trajectory)
            node.car_queue.append(new_car)
            self.all_spawned_cars.append(new_car)

    def step(self):
        """
        Perform one step of the simulation
        """

        # loop through all the nodes, and update them
        for node in self.G.nodes:
            node.update()
        
        for node in self.ending_nodes:
            # kill all the cars that are in the ending nodes, 
            # and register their waiting time
            for _ in range(len(node.car_queue)):
                car = node.car_queue.pop(0)
                car.kill(self.time_step)
    

        for node in self.stoplight_nodes:
            
            # spawn new pedestrians and cars
            self.spawn_pedestrian(node, prob=0.1)
            self.spawn_car(node, prob=0.1)

            # pedestrian transitions (actually we kill them)
            
            #print(f"node {node.id}: stop={node.stop}, ped_queue={len(node.pedestrian_queue)}, car_queue={len(node.car_queue)}")
            
            if node.stop == True:
                # pedestrians can cross. cars cannot
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
                    and node.car_queue[0].cooldown <= 0
                ):
                    print(f"moving car from node {node.id} to node {transition_node.id}")
                    car = node.car_queue.pop(0)
                    transition_node.car_queue.append(car)
                    car.cooldown = 5
        
        for node in self.transition_nodes:
            # move the first car to the next node, but only if
            # the next node is not at max capacity
            next_node = list(self.G.successors(node))[0]
            if (node.stop == False 
                and len(node.car_queue) > 0
                and (type(next_node) is EndingNode or len(next_node.car_queue) <= next_node.max_capacity)
            ):
                car = node.car_queue.pop(0)
                next_node.car_queue.append(car)
        
        for node in self.yield_nodes:
            next_node = list(self.G.successors(node))[0]

        self.time_step += 1
