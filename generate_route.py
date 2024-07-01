import networkx as nx
import random
import matplotlib.pyplot as plt
import math
import numpy as np
from numpy import arange
from typing import List
import time

from route import Route_Window


        #for number of groups == 4
        #v0 = 0.1 - 0.16
        #v1 = 0.16 - 0.35
        #v2 = 0.35 - 0.65


class GeneratedRoute(Route_Window):


    def __init__():
        return


    def generate_and_convert_route(self,):

        G = self.generate_grouped_graph(4)
        spring_const = random.uniform(0.1, 0.16)

        pos = self.fruchterman_reingold(G,alpha=spring_const)
        pos, start_node, end_node = self.rotate_graph(pos)




    def generate_grouped_graph(self,max_groups=3):
        G = nx.Graph()



        total_nodes = 0
        total_edges = 0

        group_nodes = {}

        prev_group = 1

        for group in range(1, max_groups + 1):

            num_nodes = random.randint(3, 5)

            nodes = [(f'group_{group}_{i}', {'group': group}) for i in range(1, num_nodes + 1)]
            G.add_nodes_from(nodes)

            group_nodes[group] = [f'group_{group}_{i}' for i in range(1, num_nodes + 1)]

            for i in range(1, num_nodes + 1):
                num_edges = random.randint(1, 4)

                sample_size = min(num_edges, num_nodes - 1)

                possible_targets = [n for n in group_nodes[group] if n != f'group_{group}_{i}']
                edges = [(f'group_{group}_{i}', target) for target in random.sample(possible_targets, sample_size)]

                G.add_edges_from(edges)

            total_nodes += num_nodes
            total_edges += num_nodes * 4  # Maximum possible edges for each node in the group

            # Connect the group to a previously observed group using breadth-first addition
            if group > 1:

                connecting_edges = random.randint(2, 4)
                for i in range(connecting_edges):
                # Select nodes from the two groups
                    while(True):
                        node1 = random.choice(group_nodes[prev_group])
                        node2 = random.choice(group_nodes[group])

                        if G.has_edge(node1, node2):
                            continue
                        # Add an edge between the selected nodes
                        G.add_edge(node1, node2)
                        break

            # Add the current group to the queue
            prev_group = group

        return G





    # attractive force
    def f_a(self,d,k):
        return d*d/k

    # repulsive force
    def f_r(self,d,k):
        return k*k/d

    def fruchterman_reingold(self,G,iteration=50, alpha=1.0):
        W = 1
        L = 1
        area = W*L

        k = alpha*math.sqrt(area/len(list(G.nodes())))

        # initial position
        for v in list(G.nodes):
            G.nodes[v]['x'] = W*random.random()
            G.nodes[v]['y'] = L*random.random()


        t = W/10
        dt = t/(iteration+1)

        #print("area:{0}".format(area))
        #print("k:{0}".format(k))
        #print("t:{0}, dt:{1}".format(t,dt))

        for i in range(iteration):
            #print("iter {0}".format(i))

            pos = {}
            for v in list(G.nodes):
                pos[v] = [G.nodes[v]['x'],G.nodes[v]['y']]
            # plt.close()
            # plt.ylim([-0.1,1.1])
            # plt.xlim([-0.1,1.1])
            # plt.axis('off')
            # nx.draw_networkx(G,pos=pos,node_size=10,width=0.1,with_labels=False)
            #plt.savefig("{0}.png".format(i))

            # calculate repulsive forces
            for v in list(G.nodes):
                G.nodes[v]['dx'] = 0
                G.nodes[v]['dy'] = 0
                for u in list(G.nodes()):
                    if v != u:
                        dx = G.nodes[v]['x'] - G.nodes[u]['x']
                        dy = G.nodes[v]['y'] - G.nodes[u]['y']
                        delta = math.sqrt(dx*dx+dy*dy)
                        if delta != 0:
                            d = self.f_r(delta,k)/delta
                            G.nodes[v]['dx'] += dx*d
                            G.nodes[v]['dy'] += dy*d

            # calculate attractive forces
            for v,u in list(G.edges):
                dx = G.nodes[v]['x'] - G.nodes[u]['x']
                dy = G.nodes[v]['y'] - G.nodes[u]['y']
                delta = math.sqrt(dx*dx+dy*dy)
                if delta != 0:
                    d = self.f_a(delta,k)/delta
                    ddx = dx*d
                    ddy = dy*d
                    G.nodes[v]['dx'] += -ddx
                    G.nodes[u]['dx'] += +ddx
                    G.nodes[v]['dy'] += -ddy
                    G.nodes[u]['dy'] += +ddy

            # limit the maximum displacement to the temperature t
            # and then prevent from being displace outside frame
            for v in list(G.nodes):
                dx = G.nodes[v]['dx']
                dy = G.nodes[v]['dy']
                disp = math.sqrt(dx*dx+dy*dy)
                if disp != 0:
                    #cnt += 1
                    d = min(disp,t)/disp
                    x = G.nodes[v]['x'] + dx*d
                    y = G.nodes[v]['y'] + dy*d
                    x =  min(W,max(0,x)) - W/2
                    y =  min(L,max(0,y)) - L/2
                    G.nodes[v]['x'] = min(math.sqrt(W*W/4-y*y),max(-math.sqrt(W*W/4-y*y),x)) + W/2
                    G.nodes[v]['y'] = min(math.sqrt(L*L/4-x*x),max(-math.sqrt(L*L/4-x*x),y)) + L/2

            # cooling
            t -= dt

        pos = {}
        for v in list(G.nodes):
            pos[v] = [G.nodes[v]['x'],G.nodes[v]['y']]
        # plt.close()
        # plt.ylim([-0.1,1.1])
        # plt.xlim([-0.1,1.1])
        # plt.axis('off')
        # nx.draw_networkx(G,pos=pos,node_size=10,width=0.1,with_labels=False)
        # plt.savefig("{0}.png".format(i+1))

        return pos

    def euclaidian_dist(self,p1,p2):
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        return dist


    def longest_distance(self,pos):

        longest_dist = 0
        start_node = -1
        end_node = -1
        for v, v_pos in list(pos.items())[:4]:
            for u , u_pos in list(pos.items())[len(pos.items())//3*2:]:
                dist = self.euclaidian_dist(v_pos,u_pos)
                if dist > longest_dist:
                    start_node = v
                    end_node = u
                    longest_dist = dist


        return start_node , end_node

    def rotate_point(self,point, angle, center):
        """Rotate a point around a center by a given angle."""
        angle_rad = np.radians(angle)
        x, y = point
        cx, cy = center

        new_x = cx + (x - cx) * np.cos(angle_rad) - (y - cy) * np.sin(angle_rad)
        new_y = cy + (x - cx) * np.sin(angle_rad) + (y - cy) * np.cos(angle_rad)

        return [new_x, new_y]

    def plot_line(start, end, angle):
        """Plot the rotated line."""
        plt.figure(figsize=(8, 8))

        # Plot the original line
        plt.plot([start[0], end[0]], [start[1], end[1]], 'r-', label='Original Line')

        # Center of the line
        center = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)

        # Rotate the start point by the optimal angle
        rotated_start = self.rotate_point(start, angle, center)
        rotated_end = self.rotate_point(end, angle, center)

        # Plot the rotated line
        plt.plot([rotated_start[0], rotated_end[0]], [rotated_start[1], rotated_end[1]], 'b-', label='Rotated Line')

        plt.scatter([start[0], end[0]], [start[1], end[1]], c=['g', 'r'], zorder=5)
        plt.scatter([rotated_start[0], rotated_end[0]], [rotated_start[1], rotated_end[1]], c=['g', 'r'], zorder=5)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Line Rotation')
        plt.legend()
        plt.grid(True)
        plt.show()
        # time.sleep(1)
        plt.close()


    def find_optimal_rotation(self,start, end):
        """Find the optimal rotation angle to minimize the x component difference."""
        # Center of the line
        center = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)



        # Define angle range and step
        angles = range(0,360, 1)

        # Store rotated points and their x component differences
        diffs = []

        for angle in angles:
            rotated_start = self.rotate_point(start, angle, center)
            rotated_end = self.rotate_point(end, angle, center)

            x_diff = abs(rotated_start[0]-rotated_end[0])
            y_diff = rotated_end[1] - rotated_start[1]
            diffs.append((angle, x_diff, y_diff))

        # Sort by x component difference
        diffs = sorted(sorted(diffs, key = lambda x : x[1]), key = lambda x : x[2], reverse = True)


        # Get the optimal rotation angle
        optimal_angle = diffs[0][0]

        #plot_line(start,end, optimal_angle)


        return optimal_angle, center




    def rotate_graph(self,pos):


        start_node, end_node = self.longest_distance(pos)
        start = pos[start_node]
        end = pos[end_node]


        best_angle, center = self.find_optimal_rotation(start,end)
        #print(best_angle)

        pos_new = {key:self.rotate_point(value, best_angle, center) for key,value in pos.items()}


        return pos_new, start_node, end_node




    def scale_graph(self,pos, new_min_x, new_max_x):

        Xs = [value[0] for value in pos.values()]
        Ys = [value[1] for value in pos.values()]

        x_min = min(Xs)
        x_max = max(Xs)
        y_min = min(Ys)
        y_max = max(Ys)

        ratio = (x_max-x_min) / (new_max_x- new_min_x)






        for key,value in pos.items():
            new_x = self.scale_value(value[0], x_min, x_max, new_min_x, new_max_x)
            new_y = value[1] * ratio

            pos[key] = [new_x, new_y]

        return pos
    
    def scale_value(self, value, old_min, old_max, new_min, new_max):
        scaled_value = new_min + (((value - old_min) * (new_max - new_min)) / (old_max - old_min))
        return scaled_value





