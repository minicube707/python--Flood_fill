import numpy as np
import pygame
import random


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Flood fill Path finding Algorithm")


#Color in RGB
BLACK =         (0, 0, 0)
GREY =          (128, 128, 128)
WHITE =         (255, 255, 255)

RED =           (255, 0, 0)
GREEN =         (0, 255, 0)
BLUE =          (0, 0, 255)

YELLOW =        (255, 255, 0)
CYAN =          ( 0, 255, 255)
PURPLE =        (255, 0, 255)

ORANGE =        (255, 165, 0)


#Function which applies a condition to the neighbors of the node
def for_neighbors (grid, current_node, size, index, condition, option):
    list_delta = [-1, 1]

    for delta in list_delta:
        if 0 <= (current_node[index] + delta ) < size:
            option = condition(grid, current_node, delta, option)

    return option


#See if the node at the left and at the right are walls and update the grid adding the walls
def scann_wall_horizontal (grid, current_node, delta, set_wall):

    #If there a wall next to the node, mark it
    if (current_node[0], current_node[1] + delta) in set_wall:
        grid[current_node[0], current_node[1] + delta] = -1

    return set_wall


#See if the node at the top and at the bottom are walls and update the grid adding the walls
def scann_wall_vertical (grid, current_node, delta, set_wall):

    #If there a wall next to the node, mark it
    if (current_node[0] + delta, current_node[1]) in set_wall:
        grid[current_node[0] + delta, current_node[1]] = -1

    return set_wall


#Scann the neighbors and return True if the path is correct
def scann_path_horizontal (grid, current_node, delta, follow_path):
    current_val = grid[current_node]

    #If the the neighbors follow the path
    if grid[current_node[0], current_node[1] + delta] == current_val - 1:
        follow_path = True

    return follow_path


#Scann the neighbors and return True if the path is correct
def scann_path_vertical (grid, current_node, delta, follow_path):
    current_val = grid[current_node]

    #If the the neighbors follow the path
    if grid[current_node[0] + delta, current_node[1]] == current_val - 1:
        follow_path = True

    return follow_path


#Search the minimum value at the left and right of the node
def search_min_horizontal (grid, node, delta, min):

    #If the value is smallest than min
    if 0 < grid[node[0], node[1] + delta] < min:
        min = grid[node[0], node[1] + delta]

    return min


#Search the minimum value at the top and bottom of the node
def search_min_vertical (grid, node, delta, min):

    #If the value is smallest than min
    if 0 < grid[node[0] + delta, node[1]] < min:
        min = grid[node[0] + delta, node[1] ]

    return min


#Function adding value to the neighbors at the left and right
def make_grid_horizontal (grid, node, delta, list_next_node):
    current_val = grid[node]

    #If the neighbors is zeros, his new value is this of the current node plus one
    if grid[node[0], node[1] + delta] == 0:
        grid[node[0], node[1] + delta] = current_val + 1
        list_next_node.append((node[0], node[1] + delta))

    return list_next_node


#Function adding value to the neighbors at the top and bottom
def make_grid_vertical (grid, node, delta, list_next_node):
    current_val = grid[node]

    #If the neighbors is zeros, his new value is this of the current node plus one
    if grid[node[0] + delta, node[1]] == 0:
        grid[node[0] + delta, node[1]] = current_val + 1
        list_next_node.append((node[0] + delta, node[1]))

    return list_next_node


#Function adding this neighbors on the horizontal axis on the list
def refresh_grid_horizontal (grid, node, delta, list_neighbors):

    #If the nieghbors isn't a wall, add it in the list
    if grid[node[0], node[1] + delta] != -1:
        neigbhors_node = (node[0], node[1] + delta)
        list_neighbors.append(neigbhors_node)

    return list_neighbors


#Function adding this neighbors on the vertical axis on the list
def refresh_grid_vertical (grid, node, delta, list_neighbors):
    
    #If the nieghbors isn't a wall, add it in the list
    if grid[node[0] + delta, node[1]] != -1:    
        neigbhors_node = (node[0] + delta, node[1])
        list_neighbors.append(neigbhors_node)

    return list_neighbors 


#Function who the algorithm choose a direction to closer the objectif
def chose_direction (grid, current_node, size):
    list_delta = [-1, 1]
    min_val = float("inf")
    dir_val = 0

    #Left Right
    for index, delta in enumerate (list_delta):
        if 0 <= (current_node[1] + delta ) < size:

            if 0 <= grid[current_node[0], current_node[1] + delta] < min_val:    
                min_val = grid[current_node[0], current_node[1] + delta]
                dir_val = index 
  
    #Up Down
    for index, delta in enumerate (list_delta):
        if 0 <= (current_node[0] + delta) < size:

            if 0 <= grid[current_node[0] + delta, current_node[1]] < min_val:
                min_val = grid[current_node[0] + delta, current_node[1]]
                dir_val = index + 2


    #Left 
    if dir_val == 0:
        current_node = (current_node[0], current_node[1] - 1)

    #Right
    elif dir_val == 1:
        current_node = (current_node[0], current_node[1] + 1)

    #Up 
    elif dir_val == 2:
        current_node = (current_node[0] - 1, current_node[1])
    
    #Down
    else:
        current_node = (current_node[0] + 1, current_node[1])

    return current_node


#Function scann his neighbors, to search the wall, and to built the path
def scann_neigbhors (grid, current_node, size, set_wall):
    follow_path = False
    run = True

    #Update the grid if the neighbors is a wall
    for_neighbors(grid, current_node, size, 1, scann_wall_horizontal, set_wall)    #Left Right
    for_neighbors(grid, current_node, size, 0, scann_wall_vertical, set_wall)      #Up Down

    #See if the path didn't loss
    follow_path = for_neighbors(grid, current_node, size, 1, scann_path_horizontal, follow_path)    #Left Right
    follow_path = for_neighbors(grid, current_node, size, 0, scann_path_vertical, follow_path)      #Up Down
    
    if not follow_path:
        grid, run = refresh_grid(grid, current_node, size)

    return grid, run


#See the neighbors if the neighbors not follow update them thus his neighbors
def refresh_grid (grid, current_node, size):

    list_neighbors = []
    list_neighbors.append(current_node)
    run = True

    #While there is node to update
    while len(list_neighbors) > 0:

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if run:
            #Initialisation
            min = float("inf")
            node = list_neighbors[0]
            current_val = grid[node]

            #Search the min value among the neighbors
            min = for_neighbors(grid, node, size, 1, search_min_horizontal, min)    #Left Right
            min = for_neighbors(grid, node, size, 0, search_min_vertical, min)      #Up Down

            #If the minimun value isn't this of the current node minus one, the path is loss and we must to rebuild 
            if min != current_val -1:
            
                grid[node] = (min +1)
                list_neighbors = for_neighbors(grid, node, size, 1, refresh_grid_horizontal, list_neighbors)     #Left Right
                list_neighbors = for_neighbors(grid, node, size, 0, refresh_grid_vertical, list_neighbors)       #Up Down

            #At the delete the node, we see
            list_neighbors.pop(0)

    return grid, run


#Make the grid
def make_grid (grid, end, size):
    list_node = [end]

    #While there is node to update
    while len(list_node) > 0:
        list_next_node = []

        #For the node in list, update them and add his neighbors in the next list
        for node in list_node:
            list_next_node = for_neighbors(grid, node, size, 1, make_grid_horizontal, list_next_node)   #Left Right
            list_next_node = for_neighbors(grid, node, size, 0, make_grid_vertical, list_next_node)     #Up Down


        list_node = []
        list_node = list_next_node 

    grid[end] = 0

    return grid

#Draw the grid
def draw_grid (win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


#Draw the node
def draw (win, rows, width, start, end, pathfinder, set_wall, set_path, set_explore_path):
    win.fill(WHITE)
    gap = width // rows

    for explore in set_explore_path:
        pygame.draw.rect(win, GREEN, (explore[1]*gap, explore[0]*gap,  gap, gap))

    if isinstance(start, tuple):  
        pygame.draw.rect(win, ORANGE, (start[1]*gap, start[0]*gap,  gap, gap))

    if isinstance(end, tuple):
        pygame.draw.rect(win, CYAN, (end[1]*gap, end[0]*gap,  gap, gap))
    
    if isinstance(pathfinder, tuple):
        pygame.draw.rect(win, BLUE, (pathfinder[1]*gap, pathfinder[0]*gap,  gap, gap))
    
    for wall in set_wall:
        pygame.draw.rect(win, BLACK, (wall[1]*gap, wall[0]*gap,  gap, gap))
    
    for paht in set_path:
        pygame.draw.rect(win, PURPLE, (paht[1]*gap, paht[0]*gap,  gap, gap))

    draw_grid(win, rows, width)
    pygame.display.update()


#Make the maze
def make_maze(win, width, rows, set_wall, nb_door):

    #Fill wall the maze with wall
    for i in range(rows):
        for j in range(rows):
            set_wall.add((i, j))

    #Initialsation     
    start_node, rand = place_start(rows)
    set_wall.remove(start_node)
    current_node = start_node
    history_node =  []
    history_node.append(current_node)

    #While there is node in history_node, the maze isn't fill
    empty = True
    while empty:
        
        draw(win, rows, width, start_node, None, current_node, set_wall, {}, {})
        list_direction =  [0, 1, 2, 3]

        for _ in range(5):
            
            #Search  if the neighbors are walls, in the four direction
            if len(list_direction) > 0:
                orientation = random.choice(list_direction)
 
                #Down
                if orientation == 0:
                    #Is the neighbors is a wall ?
                    if current_node[0] +2 < rows -1 and (current_node[0] + 2, current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] + 1, current_node[1], current_node[0] + 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Up
                elif orientation == 1:
                    #Is the neighbors is a wall ?
                    if current_node[0] -2 > 0 and (current_node[0] - 2 ,current_node[1]) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0] - 1, current_node[1], current_node[0] - 2, current_node[1], history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Right
                elif orientation == 2:
                    #Is the neighbors is a wall ?
                    if current_node[1] + 2 < rows -1 and (current_node[0], current_node[1] +2) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0], current_node[1] + 1, current_node[0], current_node[1] + 2, history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

                #Left
                elif orientation == 3:
                    #Is the neighbors is a wall ?
                    if current_node[1] - 2 > 0 and (current_node[0], current_node[1] -2) in set_wall:
                        history_node, current_node, set_wall = function(set_wall, current_node[0], current_node[1] - 1, current_node[0], current_node[1] - 2, history_node)

                    #No, don't keep this direction
                    else:
                        list_direction.remove(orientation)

            #All the directions are taken
            #Go back in the path
            else:
                history_node.pop(-1)
                if len(history_node) > 0:
                    current_node = history_node[-1]

                    if current_node == start_node:
                        empty = False

                else:
                    empty = False

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return set_wall, start_node, None, False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return set_wall, start_node, None, False

    end_node = place_end(set_wall, rows, rand)

    #Add the door
    for _ in  range(nb_door):
        reset = True
        while reset:
            x = random.randint(1, rows - 2)
            y = random.randint(1, rows - 2)
            if (x, y) in set_wall and (x, y) != start_node and (x, y) != end_node:

                if ((x-1, y) in set_wall and (x+1, y) in set_wall) or ((x, y-1) in set_wall and  (x, y+1) in set_wall):
                    set_wall.remove((x, y))
                    reset = False
                    draw(win, rows, width, start_node, None, current_node, set_wall, {}, {})

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return set_wall, start_node, None, False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return set_wall, start_node, None, False
    
    return set_wall, start_node, end_node, True


#Create the path when you built the maze
def function(set_wall, x1, y1, x2, y2, history_node):
    
    node = (x1, y1)
    set_wall.remove(node)
    node = (x2, y2) 
    set_wall.remove(node)
    history_node.append(node)

    return history_node, node, set_wall


#Place the start node
def place_start(rows):

    space = 0 
    while space%2 != 1:
        rand = random.randint(0, 3)
        space = random.randint(0, rows - 1)

    #Left
    if rand == 0:
        node = (0, space )
    
    #Right
    elif rand == 1:
        node = (rows - 1, space)

    #Up
    elif rand == 2:
        node = (space, 0)

    #Down
    else:
        node = (space, rows - 1)
    
    return node, rand


#Place the end node
def place_end(set_wall, rows, rand):

    #Left
    placed_end = False
    i = 1
    if rand == 0:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        
                        #If is itself pass
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (rows - 1 - i + dx, j + dy) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (rows - 1 - i, j)
                    placed_end = True

                j +=1
            i +=1
                      
    #Right
    elif rand == 1:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (i + dx, j + dy) in set_wall:
                            state_neighbors += 1

                if state_neighbors == 7:
                    end_node = (i, j)
                    placed_end = True

                j +=1
            i +=1

    #Up
    elif rand == 2:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (j + dy, rows - 1 - i + dx) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (j, rows - 1 - i)
                    placed_end = True

                j +=1
            i +=1        

    #Down
    elif rand == 3:
        while (i <= rows -1) and not placed_end:
            j = 1

            while (j <= rows -1) and not placed_end:

                state_neighbors = 0
                #For the eight neigbords of the node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        
                        #If the neighbors is a barreir 
                        if (j + dx, i + dy) in set_wall:
                            state_neighbors += 1

                #If the node has 7 node who is barrier next to him, place the end node
                if state_neighbors == 7:
                    end_node = (j, i)
                    placed_end = True

                j +=1
            i +=1

    return  end_node

#Algoritm to search the smallest path between two points
def algorithm (win, grid, width, rows, start, end, set_wall, set_explore_path):
    current_node = start
    run = True

    #While we isn't in the place where the value is zeros , run
    while grid[current_node] != 0:

        #Scann the neighbors, update the grid
        grid, run = scann_neigbhors(grid, current_node, rows, set_wall)

        #Then the grid updte chose a direction
        current_node =  chose_direction(grid, current_node, rows)

        if current_node not in set_explore_path:
            set_explore_path.add(current_node)

        draw(win, rows, width, start, end, current_node, set_wall, {}, set_explore_path)

    return run


#Algorithm to draw the path
def algorithm_path (win, grid, width, rows, start, end,  set_wall, set_path):
    current_node = start

    while grid[current_node] != 1:
        current_node =  chose_direction(grid, current_node, rows)
        set_path.add(current_node)

        draw(win, rows, width, start, end, None, set_wall, set_path, {})


#Retrun the position in the grid, of the position of the mouse
def get_clicked_pos (pos, rows, width):

    x, y = pos
    gap = width // rows
    row = x // gap
    col = y // gap

    return row, col


#Add node in the grid
def add_node (width, rows, start, end, set_wall):

    #Left click
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width):
            row, col = get_clicked_pos(pos, rows, width)
            node = (col, row)

            if not start and node != end:
                start = node

            elif not end and node != start:
                end = node

            elif node != end and node != start:
                set_wall.add(node)
    
    return start, end, set_wall


#Delete node in the grid
def delete_node (width, rows, start, end, set_wall):

    #Right click
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width):
            row, col = get_clicked_pos(pos, rows, width)
            node = (col, row)

            if node == start:
                start = None
    
            if node == end:
                end = None
    
            if node in set_wall:
                set_wall.remove(node)

    return start, end, set_wall

#Main algorithm
def main (win , width):

    rows = 50

    #Wall == -1
    set_wall = set()
    set_path = set()

    #END == 0
    start = None
    end = None

    nb_door = 50

    run = True
    while run:
        
        #Pygame event
        for event in pygame.event.get():
            
            #Place the node in the grid
            start, end, set_wall = add_node(width, rows, start, end, set_wall)      #Left click
            start, end, set_wall = delete_node(width, rows, start, end, set_wall)   #Right click
            draw(win, rows, width, start, end, None, set_wall, set_path, {})

            #Quit pygame
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                #Make the  maze
                if event.key == pygame.K_g:
                    set_wall, start, end, run = make_maze(win, width, rows, set_wall, nb_door)
                    
                #Search the smallest path
                if event.key == pygame.K_SPACE and start and end:
                    if run:
                        
                        #Initialisation
                        set_path.clear()
                        set_explore_path = set()
                        go_grid = np.zeros((rows, rows), int)
                        back_grid = np.zeros((rows, rows), int)
                        one_time = False
                        two_time = False

                        #Verify two time than the path is clear
                        while not two_time:

                            #GO
                            go_grid = np.zeros((rows, rows), int)           #Initialise the grid
                            go_grid[-1 == back_grid] = -1                   #Save the wall already find
                            go_grid = make_grid(go_grid, end, rows)         #Make the grid with the with the walls find 
                            algorithm(win, go_grid, width, rows, start, end, set_wall, set_explore_path)

                            #Back  
                            back_grid = np.zeros((rows, rows), int)         #Initialise the grid
                            back_grid[-1 == go_grid] = -1                   #Keep the emplacement of the wall discorver
                            back_grid = make_grid(back_grid, start, rows)   #Make the grid with the with the walls find
                            algorithm(win, back_grid, width, rows, end, start, set_wall, set_explore_path)

                            #Initialise the grid, but saving the emplacement of the walls
                            back_grid[0 < back_grid] = 0
                            back_grid = make_grid(back_grid, end, rows)

                            #Vérify if the algorithm has done two time the same go back

                            if np.array_equal(go_grid, back_grid) and one_time:
                                two_time = True
                            elif np.array_equal(go_grid, back_grid):
                                one_time = True
                            else:
                                one_time = False


                        #Draw the path
                        #Keep the emplacement of the wall discorver
                        go_grid[0 < go_grid] = 0
                        go_grid = make_grid(go_grid, end, rows)
                        algorithm_path(win, go_grid, width, rows, start, end, set_wall, set_path)
                    

                #New grid
                if event.key == pygame.K_n:
                    set_path.clear()
                    set_wall.clear()
                    start = None
                    end = None    

                #Clear the grid
                if event.key == pygame.K_c:
                    set_path.clear()
                    

                draw(win, rows, width, start, end, None, set_wall, set_path, {})

    pygame.quit()

main(WIN, WIDTH)