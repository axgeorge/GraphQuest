"""
INTERACTIVE EULERIAN TOUR EXPLORER

INSTRUCTIONS:
- Right-click to place a **vehicle depot** (black).
- Left-click to place a **target node** (red).
- Press **SPACEBAR** to generate Eulerian tours.
- Press **C** to clear the grid and try again.

FEATURES:
- **Multi-vehicle routing** using minimum spanning trees.
- **Eulerian tour generation** with directional edge coloring (forward = black, return = green).
- Flexible and interactive — define your own scenarios in real time!
"""

import pygame
import math
from collections import defaultdict

WIDTH = 800 # the width of our square map
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("EULERIAN TOUR EXPLORER")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Define a class for an arbitrary point on the map as shown below

class Point:
    def __init__(self, row, col, width): # width here is the width of the square cell
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width

    def make_target(self):
        self.color = RED

    def make_vehicle(self):
        self.color = BLACK

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


def make_cells(rows, width): # width here is the size of the entire grid display
    """
    Define each cell in the grid display. A cell is a point object defined by its row, col, and size.
    """
    cells = []
    increment = width // rows
    for i in range(rows):
        cells.append([])
        for j in range(rows):
            point = Point(i, j, increment)
            cells[i].append(point)

    return cells


def draw_grid(win, rows, width): # win here is the display object and width is the size of the display
    """
    Draw the vertical and horizontal lines defining the grid. Called in the draw function.
    """
    increment = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * increment), (width, i * increment))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * increment, 0), (j * increment, width))


def draw(win, cells, rows, width): # win here is the display object and width is the size of the display
    """
    Fill the entire display white, then color each cell based on the values assigned to them. Finally draw grid lines.
    This will be called once each frame in the main while loop.
    """
    win.fill(WHITE)
    for row in cells:
        for point in row:
            point.draw(win)
    draw_grid(win, rows, width)


def get_clicked_pose(pos, rows, width):
    """
    A function to find the cell associated with a point clicked by the user.
    """
    increment = width // rows
    y, x = pos
    row = y // increment
    col = x // increment
    return row, col


def gen_obj_edges(obj_nodes, node_type):
    """
    Given a list of nodes (point objects), generate the list of undirected edges for the complete graph.
    """
    obj_edges = []
    for i in range(len(obj_nodes)):
        for j in range(i+1, len(obj_nodes)): # only upper triangle of the matrix
            u, v = obj_nodes[i], obj_nodes[j]
            if node_type[i] == 1 and node_type[j] == 1: # both are vehicle nodes
                weight = 0
            else:
                x1 = u.x + u.width/2
                y1 = u.y + u.width/2
                x2 = v.x + v.width/2
                y2 = v.y + v.width/2
                weight = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            obj_edges.append([u, v, weight])
    return obj_edges


def min_spanning_tree(obj_nodes, obj_edges):
    """
    Given a graph, return Kruskal's Minimum Weight Spanning Tree for that graph.
    """

    parent = {node: node for node in obj_nodes}
    rank = {node: 0 for node in obj_nodes}
    
    def find(node):
        """
        Find function finds the group to which a node belongs. It does it by identifying the
        representative (root) of the group the node belongs to. Two nodes belong to the
        same group iff they are connected since they both are connected to the root. Hence, adding
        an edge between such node pairs will lead to cycles.
        """
        if parent[node] != node:
            parent[node] = find(parent[node]) # The assignment compresses path from node to root. Every node in the path finally points directly at root.
        return parent[node]
    
    def union(node1, node2):
        """
        Union function combines two groups. It does this by placing the root of one
        group as the child of the root of the other group.
        
        The 'rank' heuristic is used to keep the tree shallow by always attaching
        the shorter tree under the root of the taller tree. Note that the rank of the root of
        a tree represents an upper bound on the height of the tree and is used only to guide
        efficient union operations; it may not always reflect the exact height of the tree.
        """
        root1 = find(node1)
        root2 = find(node2)

        if root1 == root2:
            return

        if rank[root1] < rank[root2]:
            parent[root1] = root2

        elif rank[root2] < rank[root1]:
            parent[root2] = root1

        else:
            rank[root1] += 1
            parent[root2] = root1

    
    mstree = []
    obj_edges = sorted(obj_edges, key=lambda x: x[2])
    for [u, v, w] in obj_edges:
        if find(u) != find(v):
            union(u, v)
            mstree.append([u, v, w])

    return mstree


def gen_adj_list(edges):
    """
    Get an adjacency list for a graph represented as a list of edges.
    """
    adj_lst = defaultdict(list)
    for [u, v, w] in edges:
        adj_lst[u].append(v)
        adj_lst[v].append(u)
    return adj_lst


def dfs(root, adj_lst, path, visited):
    """
    Depth first search.
    """
    if root not in visited:
        visited.add(root)
        path.append(root)
        for node in adj_lst[root]:
            dfs(node, adj_lst, path, visited)


def eul_tour(root, adj_lst, tour_eul, visited):
    """
    Given a tree, use a DFS variant to obtain a double-edged walk that traverse all
    nodes in the tree twice in opposite directions. Same as an Eulerian tour on the
    tree if all its edges were doubled.
    """
    if root not in visited:
        visited.add(root)
        tour_eul.append(root)
        for node in adj_lst[root]:
            if node not in visited:
                eul_tour(node, adj_lst, tour_eul, visited)
                tour_eul.append(root)


def find_veh_eul_tours(vehicles, adj_lst):
    """
    Return Eulerian tours for each vehicle by performing a DFS variant from each vehicle.
    """
    tours = list()
    for vehicle in vehicles:
        tour_eul = []
        eul_tour(vehicle, adj_lst, tour_eul, set())
        tours.append(tour_eul)
    return tours


def find_veh_tsp_tours(vehicles, adj_lst):
    """
    Return TSP tours for each vehicle by performing a DFS from each vehicle.
    """
    tours = list()
    for vehicle in vehicles:
        tour_eul = []
        dfs(vehicle, adj_lst, tour_eul, set())
        tour_eul.append(tour_eul[0]) # return to start
        tours.append(tour_eul)
    return tours


def main(win, width):
    
    ROWS = 50
    increment = width // ROWS
    cells = make_cells(ROWS, width)

    run = True # know if you started the main loop
    solved = False # is the problem solved yet?
    nodes = []
    binary = [] # keep track of whether a node is a vehicle node or target node
    result = []

    while run:
        draw(win, cells, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_presses = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pose(pos, ROWS, width)
                point = cells[row][col]
                nodes.append(point)
                
                if mouse_presses[0]: # Left click
                    point.make_target()
                    binary.append(0)
                elif mouse_presses[2]: # Right click
                    point.make_vehicle()
                    binary.append(1)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    def fix_adjacency_list(adjlist, binary):
                        """
                        Removes edges between vehicle nodes from the adjacency list.
                        """
                        node_to_index = {nodes[i]: i for i in range(len(nodes))}
                        for i in range(len(binary)):
                            if binary[i] == 1: # ith node is a vehicle
                                vi = nodes[i]
                                for node in adjlist[vi][:]:  # Iterate over a copy to avoid issues during removal
                                    if binary[node_to_index[node]] == 1:
                                        adjlist[vi].remove(node)
                                        adjlist[node].remove(vi)  # Ensure undirected edge is removed both ways
                        return adjlist
                    
                    vehicles = set()
                    for i in range(len(binary)):
                        if binary[i] == 1:
                            vehicles.add(nodes[i])

                    edges = gen_obj_edges(nodes, binary)
                    mstree = min_spanning_tree(nodes, edges)
                    adjlist = gen_adj_list(mstree)
                    adjlist = fix_adjacency_list(adjlist, binary)
                    tours = find_veh_eul_tours(vehicles, adjlist)
                    # tours = find_veh_tsp_tours(vehicles, adjlist)
                    
                    result.clear()
                    for tour in tours:
                        for i in range(1, len(tour)):
                            result.append((tour[i - 1], tour[i]))
                    solved = True
                    

                if event.key == pygame.K_c: # Press c to clear screen
                    cells = make_cells(ROWS, width)
                    nodes.clear()
                    binary.clear()
                    result.clear()
                    solved = False
                    
        if not solved: # if not solved yet, do not display result
            pass
                
        else:
            shift_amount = 3  # pixels to shift up/down

            for tour in tours:
                visited_nodes = set()
                visited_nodes.add(tour[0])  # Mark starting node as visited

                for i in range(1, len(tour)):
                    u = tour[i - 1]
                    v = tour[i]

                    x1 = u.x + (increment // 2)
                    y1 = u.y + (increment // 2)
                    x2 = v.x + (increment // 2)
                    y2 = v.y + (increment // 2)

                    # Check if edge is forward or backward
                    if v not in visited_nodes:
                        color = BLACK  # forward edge
                        visited_nodes.add(v)
                        y_shift = -shift_amount  # shift up
                    else:
                        color = GREEN  # backward edge
                        y_shift = shift_amount  # shift down

                    # Apply vertical shift to both points
                    start = (x1, y1 + y_shift)
                    end = (x2, y2 + y_shift)

                    # Draw arrowhead
                    arrow_length = 10  # length of the arrowhead line
                    arrow_angle = math.radians(30)  # angle between arrowhead lines

                    # Direction vector of the edge
                    dx = x2 - x1
                    dy = (y2 + y_shift) - (y1 + y_shift)
                    angle = math.atan2(dy, dx)

                    # Arrowhead points
                    arrow_tip = (x2, y2 + y_shift)
                    left_arrow = (
                        x2 - arrow_length * math.cos(angle - arrow_angle),
                        (y2 + y_shift) - arrow_length * math.sin(angle - arrow_angle)
                    )
                    right_arrow = (
                        x2 - arrow_length * math.cos(angle + arrow_angle),
                        (y2 + y_shift) - arrow_length * math.sin(angle + arrow_angle)
                    )

                    # Draw arrowhead as a filled triangle
                    pygame.draw.polygon(win, color, [arrow_tip, left_arrow, right_arrow])
                    
                    pygame.draw.line(win, color, start, end, width=3)

        pygame.display.flip()
            
    pygame.quit()

main(WIN, WIDTH)
