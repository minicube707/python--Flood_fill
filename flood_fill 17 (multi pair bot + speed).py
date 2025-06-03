import numpy as np
import pygame
import random
import time

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
PINK =          (255,25,179)


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


#Function who the algorithm choose a direction to closer the objectif
def chose_direction (grid, current_node, size, horizontal):
    list_delta = [-1, 1]
    min_val = float("inf")
    dir_val = 0

    if horizontal:

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

    else:
        #Up Down
        for index, delta in enumerate (list_delta):
            if 0 <= (current_node[0] + delta) < size:

                if 0 <= grid[current_node[0] + delta, current_node[1]] < min_val:
                    min_val = grid[current_node[0] + delta, current_node[1]]
                    dir_val = index + 2

        #Left Right
        for index, delta in enumerate (list_delta):
            if 0 <= (current_node[1] + delta ) < size:

                if 0 <= grid[current_node[0], current_node[1] + delta] < min_val:    
                    min_val = grid[current_node[0], current_node[1] + delta]
                    dir_val = index

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
def scann_neigbhors (grid, current_node, size, run, stop, set_wall):

    #Update the grid if the neighbors is a wall
    for_neighbors(grid, current_node, size, 1, scann_wall_horizontal, set_wall)    #Left Right
    for_neighbors(grid, current_node, size, 0, scann_wall_vertical, set_wall)      #Up Down

    return run, stop

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


#Draw left grid,this represent the world
def drawn_global_vision(win, width, rows, start, end, set_wall, set_path):
    gap = width // rows
    
    for wall in set_wall:
        pygame.draw.rect(win, BLACK, (wall[1]*gap, wall[0]*gap,  gap, gap))
    
    for paht in set_path:
        pygame.draw.rect(win, PURPLE, (paht[1]*gap, paht[0]*gap,  gap, gap))

    if isinstance(start, tuple):  
        pygame.draw.rect(win, ORANGE, (start[1]*gap, start[0]*gap,  gap, gap))

    if isinstance(end, tuple):
        pygame.draw.rect(win, CYAN, (end[1]*gap, end[0]*gap,  gap, gap))


#Draw the grid
def draw_grid (win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))



#Draw the window
def draw (win, rows, width, start, end, set_wall, set_path):

    #Initialisation
    WIN.fill(WHITE)
    drawn_global_vision(win, width, rows, start, end, set_wall, set_path)
    draw_grid(win, rows, width)

    pygame.draw.line(win, BLACK, (width, 0), (width, width), 3)
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
    show = True

    #While there is node in history_node, the maze isn't fill
    empty = True
    while empty:
        list_direction =  [0, 1, 2, 3]

        if show:
            draw(win, rows, width, start_node, {}, set_wall, {})
        
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

                if event.key == pygame.K_s:
                    show = False
                
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

                    if show:
                        draw(win, rows, width, start_node, {}, set_wall, {})
                        
            
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


def bot(wall_grid, rows, run, stop, start, end, current_node, set_wall, go, save_grid, horizontal): 

    #Initialisation of grid wall, filling the grid with wall
    new_wall_grid = np.ones((rows, rows), int) * -1
    finished = False

    #GO
    if go:     
        #Add the path, to the wall grid          
        map_path = make_grid(wall_grid, end, rows)

        #Analize the neighbors of the current node, update the wall_grid, and go to the next node
        run, stop, current_node, map_path = algorithm(map_path, rows, run, stop, end, current_node, set_wall, horizontal)
        
        #Save the emplacement of the wall find, keep only the wall discover
        new_wall_grid[-1 != map_path] = 0

        #Create a safe guard of the wall map
        save_grid = None

        #If the bot find the end point
        if map_path[current_node] == 0:  
            save_grid = np.copy(new_wall_grid)
            go = False


    #Back  
    if not go: 
        
        #Add the path, to the wall grid    
        map_path = make_grid(wall_grid, start, rows)   

        #Analize the neighbors of the current node, update the wall_grid, and go to the next node             
        run, stop, current_node, map_path = algorithm(map_path, rows, run, stop, start, current_node, set_wall, not horizontal)

       #Save the emplacement of the wall find, keep only the wall discover
        new_wall_grid[-1 != map_path] = 0

        
        #If the bot find the end point
        if map_path[current_node] == 0:
            go = True  

            #If the map of the world is the same go and back, we find the shortess path
            if np.array_equal(save_grid, new_wall_grid):
                finished = True

            #Else save all the wall find in the save_grid, to another round
            else:
                save_grid = new_wall_grid

    #Return if the game is closed, if the sesseion is over, the grid update by new wall, our currently posistion, if we find the shortess path, and the grid wall of way 
    return run, stop, new_wall_grid, current_node, go, finished, save_grid


#Algoritm to search the smallest path between two points
def algorithm(grid, rows, run, stop, end, current_node, set_wall, horizontal):

    #While we isn't in the place where the value is zeros , run
    #Pygame event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                stop = not stop 

                if stop:
                    print("Stop")
                else:
                    print("Play")
                
    if run and not stop:

        #Scann the neighbors, update the grid
        run, stop = scann_neigbhors(grid, current_node, rows, run, stop, set_wall)
      
        #Refresh the grid
        #Initialisation
        new_grid = np.zeros((rows, rows), int)           
        new_grid[-1 == grid] = -1 
        new_grid = make_grid(new_grid, end, rows)
        current_node = chose_direction(new_grid, current_node, rows, horizontal)

    return run, stop, current_node, grid


#Algorithm to draw the path
def algorithm_path (win, grid, width, rows, run, stop, start, end, set_wall, set_path):
    current_node = start
    show = True
    while grid[current_node] != 1 and run and not stop:

        #Pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_SPACE:
                    stop = True 

                if event.key == pygame.K_s:
                    show = False 

        if show:
            current_node = chose_direction(grid, current_node, rows, True)
            set_path.add(current_node)
            draw(win, rows, width, start, end, set_wall, set_path)



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
        if (0 <= pos[0] <= width)  and (0 <= pos[1] <= width-1):
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

    rows = 80

    #Wall == -1
    set_wall = set()
    set_path = set()

    #END == 0
    start = None
    end = None

    nb_pair_bot = 1
    time_bt_bot = 1
    nb_door = 100

    run = True
    stop = False
    while run:

        #Pygame event
        for event in pygame.event.get():
            
            #Place the node in the grid
            start, end, set_wall = add_node(width, rows, start, end, set_wall)      #Left click
            start, end, set_wall = delete_node(width, rows, start, end, set_wall)   #Right click

            #Quit pygame
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                
                #Make the  maze
                if event.key == pygame.K_g:
                    set_path.clear()
                    set_wall, start, end, run = make_maze(win, width, rows, set_wall, nb_door)
                    
                #Search the smallest path
                if event.key == pygame.K_SPACE and start and end:
                    start_solve = time.time()
                    stop = False
                    print("Run")

                    #Initialisation
                    set_path.clear()
                    wall_grid = np.zeros((rows, rows), int)
                    
                    list_current_start = []
                    list_save_grid = []
                    list_go = []

                    for _ in range(nb_pair_bot*2):
                        list_current_start.append(start)
                        list_save_grid.append(np.zeros((rows, rows), int))
                        list_go.append(True)
                        
                    #Verify two time than the path is clear
                    finished = False
                    start_time = time.time()
                    while run and not finished:
                       
                        for i in range(nb_pair_bot):
                            current_time = time.time()
                            
                            #Add the bot in the grid only when the time betteew bot is pass
                            if (current_time - start_time) >=  (i * time_bt_bot):
                                index = i*2
                                
                                run, stop, wall_grid, list_current_start[index], list_go[index], finished, list_save_grid[index] = bot(wall_grid, rows, run, stop, start, end, list_current_start[index], set_wall, list_go[index], list_save_grid[index], True)
                                if not run or finished:
                                    break

                                run, stop, wall_grid, list_current_start[index + 1], list_go[index + 1], finished, list_save_grid[index + 1] = bot(wall_grid, rows, run, stop, start, end, list_current_start[index + 1], set_wall, list_go[index + 1], list_save_grid[index + 1], False)
                                if not run or finished:
                                    break
                        

                    #Draw the path
                    #Keep the emplacement of the wall discorver
                    end_solve = time.time()
                    print("Time to solve ", end_solve - start_solve)

                    map_path = make_grid(wall_grid, end, rows)
                    algorithm_path(win, map_path, width, rows, run, stop, start, end, set_wall, set_path)
                    

                #New grid
                if event.key == pygame.K_n:   
                    set_path.clear()
                    set_wall.clear()
                    start = None
                    end = None  
                    run = True
                    stop = False   

                #Clear the grid
                if event.key == pygame.K_c:
                    set_path.clear()
                    run = True
                    stop = False 
                   
        draw(win, rows, width, start, end, set_wall, set_path)

    pygame.quit()

main(WIN, WIDTH)