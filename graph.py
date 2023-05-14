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
a12 = InitialNode(point_converter(7.5857334281685,-10.4967569592598)) #C
c12 = Stoplight(point_converter(7.3698673333496,-6.9947783015048), red = True) #D1
d12 = Node(point_converter(7.3440745573417,-6.3141842353067)) #P1
e12 = Node(point_converter(7.3059460451904,-5.887408832075)) #O 
f12 = Node(point_converter(7.2471840046297,-5.5478948199465)) #Q1
g12 = Node(point_converter(7.1786370182653,-4.8757841472108)) #O2 
h12 = Node(point_converter(7.0779503764026,-3.9245860696794)) #Q
i12 = Node(point_converter(7.0075517331237,-2.6399408667794)) #O1 
j12 = Node(point_converter(6.9212211549286,-0.4360088089096)) #U
k12 = FinalNode(point_converter(6.93086675544329,-0.036442187715)) #D
nodelist_12 = [a12, c12, d12, e12, f12, g12, h12, i12, j12, k12] #b12 #f12,
create_edges(G, nodelist_12)
stoplights_list.append(c12)

#List from 1 to 3 (turn left)
a13 = ListNode(point_converter(7.0982450953271,-5.3228997856363)) #M1
b13 = YieldNode(point_converter(6.9187550760409,-5.135784311697)) #R
c13 = Node(point_converter(6.5335081648615,-4.937954816767)) #N
d13 = Node(point_converter(5.5785243843548,-4.8449846298414)) #M
e13 = Node(point_converter(4.0119539497933,-4.4808026920525)) #K 
f13 = Node(point_converter(2.2833441826018,-3.7828990624901)) #S
g13 = Node(point_converter(0.6330931851997,-3.084519798628)) #L
h13 = FinalNode(point_converter(0.4361206568454,-2.9355857151185), 1) #H
nodelist_13 = [e12, a13, b13, c13, d13, e13, f13, g13, h13]
create_edges(G, nodelist_13)

#List from 1 to 4 (turn right)
a14 = ListNode(point_converter(7.5600679848197,-6.0298329597677)) #E2
b14 = Node(point_converter(8.2386059807778,-5.7668901650638)) #Z1
c14 = Node(point_converter(8.934146482221,-5.7803271575225)) #S1
d14 = Node(point_converter(14.0354126046239,-5.8087016198999)) #G2
e14 = FinalNode(point_converter(14.647289039332,-5.8176163982142)) #P
nodelist_14 = [d12, a14, b14, c14, d14, e14]
create_edges(G, nodelist_14)

#List from 2 to 1 (straight) - > down
a21 = InitialNode(point_converter(6.3273454655618,-0.3134286624478)) #A1
c21 = Stoplight(point_converter(6.4838530928216,-3.5462890847714), red = True) #B1
d21 = Node(point_converter(6.5154798332493,-4.3102801564131)) #C1
e21 = Node(point_converter(6.5335081648615,-4.937954816767)) #N #List
f21 = Node(point_converter(6.5420046027074,-5.1970326566709)) #V1
g21 = Node(point_converter(6.6528615596325,-6.1014224686689)) #L1 #List
h21 = Node(point_converter(6.7128857616537,-6.8337177333283)) #T1
i21 = Node(point_converter(6.7609051232707,-8.2502889010302)) #E1
j21 = Node(point_converter(6.8651027435212,-10.1514575323055)) #I1
k21 = FinalNode(point_converter(6.8789751659345,-10.3009702155318), 1) #G
nodelist_21 = [a21, c21, d21, e21, f21, g21, h21, i21, j21, k21]
create_edges(G, nodelist_21)
stoplights_list.append(c21)

#List from 2 to 3 (turn its right) -> window left
d23 = ListNode(point_converter(6.4140487565915, -4.4816058033434))
e23 = Node(point_converter(6.3140487565915,-4.6816058033434)) #R2
#now fill the following lists in order
nodelist_23 = [d21, d23, e23, d13]
create_edges(G, nodelist_23)

#now we append only the stoplights (even if we appended them to the nodelist and to the graph already)

#List from 2 to 4 (turn its left) -> window right
d24 = ListNode(point_converter(6.7001014237499,-5.5314433015569)) #S2
e24 = YieldNode(point_converter(6.920756012423,-5.7668910975574)) #J1
nodelist_24 = [f21, d24, e24, b14]
create_edges(G, nodelist_24)

#Second nodelist : pos 1 -> pos 3
b13.node_list.append(d21)
b13.node_list.append(e21)
b13.node_list.append(e23)

e24.node_list.append(d12)
e24.node_list.append(e12)
e24.node_list.append(a14)

#List from 3 to 4 (straight) -> left to right
a34 = InitialNode(point_converter(0.0623327235562,-3.6568860011995)) #R1
b34 = Node(point_converter(1.5162345714634,-4.4395906086797)) #N1
c34 = Stoplight(point_converter(5.36420836424,-5.6743050384899)) #U1
d34 = Node(point_converter(6.10661293896,-5.770921111209)) #K1
e34 = Node(point_converter(6.6920561434004,-5.7721158744567)) #P1
f34 = Node(point_converter(6.9207563500377,-5.771170811574)) #J1
g34 = Node(point_converter(7.4619308275128,-5.7617776331923)) #O
nodelist_34 = [a34, b34, c34, d34, e34, f34, g34, b14]
create_edges(G, nodelist_34)
stoplights_list.append(c34)

#List from 3 to 1 (turn its right) -> left to down
a31 = ListNode(point_converter(6.4838949101629,-5.9443268961541)) #C1
b31 = Node(point_converter(6.6930042213835,-6.187163515636)) #L1
#c31 = ListNode(point_converter(6.7128857616537,-6.8337177333283)) #T1
nodelist_31 = [d34, a31, b31, i21] #c31,
create_edges(G, nodelist_31)

#List from 3 to 2 (turn its left) -> left to up
a32 = ListNode(point_converter(7.1490955115081,-5.5506137948892)) #Q1
b32 = YieldNode(point_converter(7.1490955115081, -5.3228997856363)) #M1
#c32 = ListNode(point_converter(7.1458469367752,-4.8774079402132)) #O2
nodelist_32 = [f34, a32, b32, h12] #c32,
create_edges(G, nodelist_32)

#List from 4 to 3 (straight) -> right to left
a43 = InitialNode(point_converter(14.0354126046239,-4.9917068968246)) #L2
b43 = Node(point_converter(12.8279649228097,-4.9499583244175)) #V
c43 = Stoplight(point_converter(8.2440191175245,-4.8936596312794)) #N2
d43 = Node(point_converter(7.6980780075727,-4.8852894167466)) #R
e43 = Node(point_converter(7.3601685154079,-4.8764639548107)) #W1 #List
f43 = Node(point_converter(7.1458469367752,-4.8774079402132)) #O2
g43 = Node(point_converter(6.468678699198,-4.8780178654791)) #N #List
nodelist_43 = [a43, b43, c43, d43, e43, f43, g43, d13]
create_edges(G, nodelist_43)
stoplights_list.append(c43)

#List from 4 to 2 (turn its right) -> right to up
a42 = ListNode(point_converter(7.356062380623,-4.6255924563512)) #Q2
nodelist_42 = [d43, a42, h12]
create_edges(G, nodelist_42)

#List from 4 to 1 (turn its left) -> right to down
a41 = ListNode(point_converter(6.829204640617,-5.054184267278)) #V1
b41 = YieldNode(point_converter(6.6997496830357,-5.3237444241446)) #S2
nodelist_41 = [f43, a41, b41, b31]
create_edges(G, nodelist_41)

b32.node_list.append(d43)
b32.node_list.append(e43)
b32.node_list.append(f43)
b32.node_list.append(a42)

b41.node_list.append(a31)
b41.node_list.append(b31)
b41.node_list.append(d34)
b41.node_list.append(e34)

nodes_with_list = [a12, a21, a34, a43,
                   a13, a14, d24, 
                   a31, a32, a41, a42
                   ]

#paths are tuple of (start_node, end_node, spawn_rate)
paths = [(a12, k12, 0.075), (a12, e14, 0.01166666666), (a12, h13, 0.005*10),
         (a21, k21, 0.115), (a21, h13, 0.00333333333), (a21, e14, 0.01833333333), 
         (a34, k12, 0.01833333333), (a34, k21, 0.01166666666), (a34, e14, 0.03666666666), 
         (a43, k12, 0.01833333333), (a43, h13, 0.06333333333), (a43, k21, 0.02333333333)
         ]
