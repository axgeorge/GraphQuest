"""
The Dijkstra's algorithm
Reference: Tech with Tim A* Tutorial on youtube.
Instruction: Run file. Select the start cell, then the end cell, then the obstacles. Undo an obstacle with right click.
Press space key to run!
Press c to reset the grid and try again.
The red cells are the expanded nodes and the green cells are the unexpanded frontier nodes.
"""

import pygame
import math
from queue import PriorityQueue

WIDTH = 800 # the width of our square map
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Shortest Path Algorithm")

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


# note that we use the manhattan distance to find the distance between the points 
# note that point = node = cell. They are equivalent


def reconstruct_path(came_from, current, draw): # This function helps visualize the shortest path from start to end!
    while current in came_from: # current is initially the end node
        current = came_from[current] # came_from[current] is the node from which the current node came
        current.make_path() # draw the computed path in the backward direction
        draw()

# DEFINE THE Dijkstra's ALGORITHM

def algorithm(draw, cells, start, end):
    count = 0 # count is to keep track of the order in which things are added to the queue
    open_set = PriorityQueue() # gives us the node with lowest g. If lowest g repeated, then lowest count!
    open_set.put((0, count, start)) # add the start node with it's g score, and count, into the priority queue
    came_from = {} # from what node, did a node come from
    g_score = {point: float("inf") for row in cells for point in row} # assume inf g scores for all the nodes except start node
    g_score[start] = 0
    

    open_set_hash = {start} # this helps us know which items are in the priority queue and not in the priority queue

    while not open_set.empty(): # if we haven't gone through all the nodes yet
        for event in pygame.event.get(): # helps us quit the algorithm if we wish
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # current node/point we are looking at = node with the lowest g score
        open_set_hash.remove(current) # to remove the node with the lowest g score. If same g scores, choose the lowest count!

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 # g score of neighbor nodes = g score of node + 1

            if temp_g_score < g_score[neighbor]: # update g score of a node only if its new g score is lower than the previous one
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash: # add neighbor node to open set hash if neighbor was not visited previously
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False # if we did not find a path!



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
    pygame.display.update()

# A function to find the cell position of the point clicked by the user

def get_clicked_pose(pos, rows, width):
    increment = width // rows
    y, x = pos
    
    row = y // increment
    col = x // increment

    return row, col

###

def main(win, width):
    ROWS = 50
    cells = make_cells(ROWS, width)

    start = None # keep track on the start and end position
    end = None

    run = True # know if you started the main loop
    started = False # know if you started the algorithm
    while run:
        draw(win, cells, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue # user should not be able to change stuff while the algorithm is running

            if pygame.mouse.get_pressed()[0]: # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pose(pos, ROWS, width)
                point = cells[row][col]
                if not start and point != end: # define the start position if it hasn't been done yet
                    start = point
                    start.make_start()

                elif not end and point != start: # define the end position if it hasn't been done yet
                    end = point
                    end.make_end()

                elif point != end and point != start: # the remaining blocks we click are the obstacles
                    point.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pose(pos, ROWS, width)
                point = cells[row][col]
                point.reset() 
                if point == start: # basically, you can reset the start and end point by right clicking
                    start == None
                elif point == end:
                    end == None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in cells:
                        for point in row:
                            point.update_neighbors(cells)

                    algorithm(lambda: draw(win, cells, ROWS, width), cells, start, end)

                if event.key == pygame.K_c: # Press c to clear screen
                    start = None
                    end = None
                    cells = make_cells(ROWS, width)
            
    pygame.quit()

main(WIN, WIDTH)

