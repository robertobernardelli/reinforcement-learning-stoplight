import networkx as nx
import math
from car import *
from nodes import *
from config import *

#the following function converts coordinates into pygame monitor pixels
def convert_point(wind_w, wind_h, img_w, img_h):
    def img_point(img_x, img_y): 
        wind_x = wind_w*img_x/img_w
        wind_y = wind_h*abs(img_y)/img_h
        if img_y > 0:
            wind_y = -wind_h*img_y/img_h
        return wind_x, wind_y
    return img_point
point_converter = convert_point(MONITOR_WIDTH, MONITOR_HEIGHT, MAP_WIDTH, MAP_HEIGHT)

G = nx.MultiDiGraph()

stoplights_list = [] #this is an extra list: here we will append only the true stoplights
rendering_list = [] #this list can be used if we eant to check the position of some nodes

def create_edges(graph, nodelist):
    graph.add_nodes_from(nodelist)
    for i in range(len(nodelist)-1):
        graph.add_edge(nodelist[i], nodelist[i+1], weight = math.dist(nodelist[i].pos, nodelist[i+1].pos))

#     2
# 3 --+-- 4
#     1

#List from 1 to 2 (straight) -> up
#a12 = InitialNode(point_converter(5.7600490180128,-31.5027881896978), 1) #E
b12 = InitialNode(point_converter(5.6033304952104,-29.9445792993286)) #F
c12 = Node(point_converter(5.151493971664,-23.4400896373767)) #G
d12 = Node(point_converter(4.5905284950229,-14.9771507967856)) #H
e12 = Stoplight(point_converter(4.2545594685764,-8.6223725911928), red = True) #I
f12 = Node(point_converter(3.7647344661156,-1.0300040700196)) #J
g12 = FinalNode(point_converter(3.7206999508595,-0.1531878922726), 1) #K
nodelist_12 = [b12, c12, d12, e12, f12, g12]
create_edges(G, nodelist_12)
stoplights_list.append(e12)

#rendering_list = [b12, c12, d12, f12, g12]

nodes_with_list = [b12]
starting_points = [b12]
ending_points = [g12]