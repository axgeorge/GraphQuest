# The MULTI VEHICLE ALGORITHM
# Pygame is required to visualize and interact with the graph. Please install pygame!!
# The majority of the code was written to enable pygame
# Instruction: Run python file. Create your own graph as follows
# Right click for vehicle (black)
# Left click for target (red)
# Edge 1 between vertex 1 and vertex 2. Edge 2 between vertex 3 and vertex 4, and so on...
# Do not left click on vehicle or vice versa
# Press the space bar to run the algorithm
# Exit program and run again to make a new graph

import pygame
import math
from queue import PriorityQueue

WIDTH = 800 # the width of our square map
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("MULTI VEHICLE ALGORITHM")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 244, 208)

# define a class for an arbitrary point on the map as shown below

class Point:
    def __init__(self, row, col, width, total_rows): # width here is the width of the square cell
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.col, self.row

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, cells):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not cells[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(cells[self.row + 1][self.col])
                
        if self.row > 0 and not cells[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(cells[self.row - 1][self.col])
                
        if self.col < self.total_rows - 1 and not cells[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(cells[self.row][self.col + 1])

        if self.col > 0 and not cells[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(cells[self.row][self.col - 1])

    def __lt__(self, other):
        return False


# define a function to define each cell within the grid map. Width here is map width
# each cell inside cells is an instance of the class Point

def make_cells(rows, width):
    cells = []
    increment = width // rows
    for i in range(rows):
        cells.append([])
        for j in range(rows):
            point = Point(i, j, increment, rows)
            cells[i].append(point)

    return cells


# define a function to draw the grid lines inside the grid map. Width here is the map width

def draw_grid(win, rows, width):
    increment = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * increment), (width, i * increment))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * increment, 0), (j * increment, width))

# for the following function, assume that we already know which row, and which point (node) inside the row.
# Note that the point is an instance of Point, based on the position of the point 
# Then we can say the following

def draw(win, cells, rows, width):
    win.fill(WHITE)
    for row in cells:
        for point in row:
            point.draw(win)

    draw_grid(win, rows, width)


# A function to find the cell position of the point clicked by the user

def get_clicked_pose(pos, rows, width):
    increment = width // rows
    y, x = pos
    
    row = y // increment
    col = x // increment

    return row, col

# function that converts vertex object to vertex index. Very helpful for analyzing stuff

def obj_to_index(G):
    V = []
    G_in = []
    for entry in G:
        g_1 = entry[0]
        g_2 = entry[1]
        V.append(g_1)
        V.append(g_2)
    V = list(set(V))
    for i in range(len(G)):
        G_in.append([V.index(G[i][0]), V.index(G[i][1]), G[i][2]]) 
    return [V, G_in]

# A function that creates an adj matrix

def create_adj_matrix(A, G_in):
    for entry in G_in:
        g_1 = entry[0]
        g_2 = entry[1]
        A[g_1][g_2] = 1
        A[g_2][g_1] = 1
    return A

# Recursion part of a depth search function

def depth_first_search(A, k, visited):
    stack = []
    stack.append(k)
    while len(stack) != 0:
        s = stack.pop()
        if visited[s] == 0:
            visited[s] = 1
        for neighbor in range(len(A)):
            if A[s][neighbor] == 1:
                if visited[neighbor] == 0:
                    stack.append(neighbor)
    print(visited)
    return visited

# A depth search function to identify different disconnected nodes of graphs

def DFS(A, visited, track):
    P = []
    for i in range(len(A)):
        visited.append(0)
    for i in range(len(visited)):
        track.append([])
        if visited[i] == 0:
            visited = depth_first_search(A, i, visited)
        for j in range(len(visited)):
            if visited[j] != 0 and j not in P:
                P.append(j)
                track[i].append(j)
    print(track)
    return track

# A function that identifies, and categorizes disconnected graphs

def disjoint_graphs_finder(G, track):
    D = []
    for i in range(len(track)):
        D.append([])
    for i in range(len(G)):
        for j in range(len(track)):
            if G[i][0] in track[j]:
                D[j].append(G[i])
    print(D)
    return(D)

# find the absolute root/parent of a node

def find(parent, node, V): 
    node = V.index(node)  # get the index corresponding to the node
    if parent[node] == node:
        return node
    return find(parent, V[parent[node]], V)

# to merge two disjoint sets
        
def union(parent, rank, node_from, node_to, V): 
    node_from_root = find(parent, node_from, V)
    node_to_root = find(parent, node_to, V)

    if rank[node_from_root] < rank[node_to_root]:
         parent[node_from_root] = node_to_root
               
    elif rank[node_to_root] < rank[node_from_root]:
        parent[node_to_root] = node_from_root
                
    else:
        parent[node_to_root] = node_from_root
        rank[node_from_root] += 1
                 
            
# THE MULTI VEHICLE ALGORITHM

def algorithm(graph, V):
    i, e = 0, 0
    parent = []
    rank = []
    result = []
    result_final = []
    graph = sorted(graph, key = lambda item: item[2])
    max_edges = len(V) - 1

    for node in range(len(V)):
        parent.append(node)
        rank.append(0)

    while e < max_edges:
        u, v, w = graph[i]
        x = find(parent, u, V)
        y = find(parent, v, V)
        i += 1

        if x != y:
            result.append([u, v, w])
            union(parent, rank, V[x], V[y], V)
            e += 1

    f = 0
    for k in range(len(result)):
        c = result[f][2]
        if c == 0:
            del result[f]
        else:
            f += 1

    [N, G_in] = obj_to_index(result)
    print(G_in)
    A = []
    for row in range(len(N)):
        A.append([])
        for col in range(len(N)):
            A[row].append(0)

    Adj = create_adj_matrix(A, G_in)
    
    C = DFS(Adj, [], [])
    print(C)

    D = disjoint_graphs_finder(G_in, C)

    for j in range(len(result)):
        result_final.append(result[j])
        result_final.append(result[j])

    return result_final 


# main function that combines the Kruskal's algorithm and the GUI

def main(win, width):
    
    ROWS = 50
    increment = width // ROWS
    cells = make_cells(ROWS, width)

    run = True # know if you started the main loop
    started = False # know if you started the algorithm
    begin = False
    coord = []
    vertices = []
    binary = [] # this is to keep track of whether an edge is a vehicle to vehicle edge, or not!

    while run:
        draw(win, cells, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue # user should not be able to change stuff while the algorithm is running

            if event.type == pygame.MOUSEBUTTONDOWN: #pygame.mouse.get_pressed()[0]: # Left mouse button
                mouse_presses = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pose(pos, ROWS, width)
                point = cells[row][col]
                vertices.append(point)
                coord.append(pos)
                if mouse_presses[0]:
                    point.make_closed()
                    binary.append(0)
                elif mouse_presses[2]:
                    point.make_barrier()
                    binary.append(1)


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    edge_length = []
                    graph = []
                    for i in range(len(coord) - 1):
                        if (i % 2) == 0:
                            p_1 = vertices[i]
                            p_2 = vertices[i + 1]
                            if binary[i] == 1 and binary[i + 1] == 1:
                                d = 0
                            else:
                                x_1 = p_1.x + (increment // 2)
                                y_1 = p_1.y + (increment // 2)
                                x_2 = p_2.x + (increment // 2)
                                y_2 = p_2.y + (increment // 2)
                                d = ((y_2 - y_1)**2 + (x_2 - x_1)**2)**0.5 # Euclidian Distance
                            edge_length.append(d)
                        
                    for j in range(len(edge_length)):
                        i = 2 * j
                        graph.append([vertices[i], vertices[i + 1], edge_length[j]])

                    V = list(set(vertices))
                    begin = True
                    algorithm(graph, V)
                    result = algorithm(graph, V)

                
        if begin is not True:
            for i in range(1, len(coord)):
                if (i % 2) != 0:
                    d = increment // 2
                    pygame.draw.line(win, RED, (vertices[i].x + d, vertices[i].y + d), 
                    (vertices[i - 1].x + d, vertices[i - 1].y + d), width = 3)

        else:
            for i in range(len(result)):
                initial = result[i][0]
                final = result[i][1]
                initial_x = initial.x + (increment // 2)
                initial_y = initial.y + (increment // 2)
                final_x = final.x + (increment // 2)
                final_y = final.y + (increment // 2)
                if (i % 2) != 0:
                    pygame.draw.line(win, BLACK, (initial_x, initial_y), (final_x, final_y), width = 3) 
                else:
                    pygame.draw.line(win, GREEN, (initial.x + (increment // 3), initial.y + (increment // 3)), 
                    (final.x + (increment // 3), final.y + (increment // 3)), width = 3) 

        pygame.display.flip()
            
    pygame.quit()

main(WIN, WIDTH)
