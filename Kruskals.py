"""
KRUSKAL'S MINIMUM SPANNING TREE ALGORITHM
Instruction: Run file. Create your own graph by clicking the desired from cell and to cell to create graph edges.
Note: The graph must be connected for the program to work. That is, there must be a path connecting any two selected cells.
To clear grid and try again, press c.
"""

import pygame

WIDTH = 800 # the width of our square map
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("KRUSKAL'S MINIMUM SPANNING TREE")

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
                 
            
# THE KRUSKAL'S ALGORITHM

def algorithm(graph, V):
    i, e = 0, 0
    parent = []
    rank = []
    result = []
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

    return result    

# main function that combines the Kruskal's algorithm and the GUI

def main(win, width):
    
    ROWS = 50
    increment = width // ROWS
    cells = make_cells(ROWS, width)

    run = True # know if you started the main loop
    begin = False
    coord = []
    vertices = []
    result = []

    while run:
        draw(win, cells, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN: #pygame.mouse.get_pressed()[0]: # Left mouse button
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pose(pos, ROWS, width)
                    point = cells[row][col]
                    vertices.append(point)
                    coord.append(pos)
                    point.make_closed()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    edge_length = []
                    graph = []
                    for i in range(len(coord) - 1):
                        if (i % 2) == 0:
                            p_1 = vertices[i]
                            p_2 = vertices[i + 1]
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
                    result = algorithm(graph, V)

                if event.key == pygame.K_c: # Press c to clear screen
                    cells = make_cells(ROWS, width)
                    vertices.clear()
                    coord.clear()
                    result.clear()
                    begin = False
        
        if not begin and len(vertices) >= 2:
            for i in range(1, len(coord)):
                if (i % 2) != 0:
                    d = increment // 2
                    pygame.draw.line(win, RED,
                                    (vertices[i].x + d, vertices[i].y + d),
                                    (vertices[i - 1].x + d, vertices[i - 1].y + d),
                                    width=3)

        else:
            for i in range(len(result)):
                initial = result[i][0]
                final = result[i][1]
                initial_x = initial.x + (increment // 2)
                initial_y = initial.y + (increment // 2)
                final_x = final.x + (increment // 2)
                final_y = final.y + (increment // 2)
                pygame.draw.line(win, BLACK, (initial_x, initial_y), (final_x, final_y), width = 3)   

        pygame.display.flip()
            
    pygame.quit()

main(WIN, WIDTH)
