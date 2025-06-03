import numpy as np

size = 5
grid_wall = np.zeros((size, size), int)


#Function which applies a condition to the neighbors of the node
def for_neighbors(grid, current_node, size, index, condition, option):
    list_delta = [-1, 1]

    for delta in list_delta:
        if 0 <= (current_node[index] + delta ) < size:
            option = condition(grid, current_node, delta, option)


    return option


#See if the node at the left and at the right are walls and update the grid adding the walls
def scann_wall_horizontal(grid, current_node, delta, follow_path):
    current_val = grid[current_node]

    #If there a wall next to the node, mark it
    if grid_wall[current_node[0], current_node[1] + delta] == 1:
        grid[current_node[0], current_node[1] + delta] = -1

    #If the the neighbors follow the path
    if grid[current_node[0], current_node[1] + delta] == current_val - 1:
        follow_path = True

    return follow_path


#See if the node at the top and at the bottom are walls and update the grid adding the walls
def scann_wall_vertical(grid, current_node, delta, follow_path):
    current_val = grid[current_node]

    #If there a wall next to the node, mark it
    if grid_wall[current_node[0] + delta, current_node[1]] == 1:
        grid[current_node[0] + delta, current_node[1]] = -1

    #If the the neighbors follow the path
    if grid[current_node[0] + delta, current_node[1]] == current_val - 1:
        follow_path = True

    return follow_path


#Search the minimum value at the left and right of the node
def search_min_horizontal(grid, node, delta, min):

    #If the value is smallest than min
    if 0 < grid[node[0], node[1] + delta] < min:
        min = grid[node[0], node[1] + delta]

    return min


#Search the minimum value at the top and bottom of the node
def search_min_vertical(grid, node, delta, min):

    #If the value is smallest than min
    if 0 < grid[node[0] + delta, node[1]] < min:
        min = grid[node[0] + delta, node[1] ]

    return min


#Function adding value to the neighbors at the left and right
def make_grid_horizontal(grid, node, delta, list_next_node):
    current_val = grid[node]

    #If the neighbors is zeros, his new value is this of the current node plus one
    if grid[node[0], node[1] + delta] == 0:
        grid[node[0], node[1] + delta] = current_val + 1
        list_next_node.append((node[0], node[1] + delta))

    return list_next_node


#Function adding value to the neighbors at the top and bottom
def make_grid_vertical(grid, node, delta, list_next_node):
    current_val = grid[node]

    #If the neighbors is zeros, his new value is this of the current node plus one
    if grid[node[0] + delta, node[1]] == 0:
        grid[node[0] + delta, node[1]] = current_val + 1
        list_next_node.append((node[0] + delta, node[1]))

    return list_next_node


#Function adding this neighbors on the horizontal axis on the list
def update_grid_horizontal(grid, node, delta, list_neighbors):

    #If the nieghbors isn't a wall, add it in the list
    if grid[node[0], node[1] + delta] != -1:
        neigbhors_node = (node[0], node[1] + delta)
        list_neighbors.append(neigbhors_node)

    return list_neighbors


#Function adding this neighbors on the vertical axis on the list
def update_grid_vertical(grid, node, delta, list_neighbors):
    
    #If the nieghbors isn't a wall, add it in the list
    if grid[node[0] + delta, node[1]] != -1:    
        neigbhors_node = (node[0] + delta, node[1])
        list_neighbors.append(neigbhors_node)

    return list_neighbors 


#Function who the algorithm choose a direction to closer the objectif
def chose_direction(grid, current_node, size):
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
def scann_neigbhors(grid, current_node, size):
    follow_path = False

    #See if the path didn't loss, and update the grid if the neighbors is a wall
    follow_path = for_neighbors(grid, current_node, size, 1, scann_wall_horizontal, follow_path)    #Left Right
    follow_path = for_neighbors(grid, current_node, size, 0, scann_wall_vertical, follow_path)      #Up Down
    
    if not follow_path:
        grid = update_grid(grid, current_node, size)

    return grid


#See the neighbors if the neighbors not follow update them thus his neighbors
def update_grid(grid, current_node, size):
    list_neighbors = []
    list_neighbors.append(current_node)

    #While there is node to update
    while len(list_neighbors) > 0:

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
            list_neighbors = for_neighbors(grid, node, size, 1, update_grid_horizontal, list_neighbors)     #Left Right
            list_neighbors = for_neighbors(grid, node, size, 0, update_grid_vertical, list_neighbors)       #Up Down

        #At the delete the node, we see
        list_neighbors.pop(0)
    return grid


#Make the grid
def make_grid(grid, end, size):
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


#Main algorithm
def main():

    grid = np.zeros((size, size), int)

    #Wall == -1
    grid_wall[0, 1] = 1
    grid_wall[1, 1] = 1
    grid_wall[2, 1] = 1
    grid_wall[3, 1] = 1


    grid_wall[1, 3] = 1
    grid_wall[2, 3] = 1
    grid_wall[3, 3] = 1

    grid_wall[1, 4] = 1

    
    #END == 0
    end = (0, 4)
    start = (0, 0)
    grid = make_grid(grid, end, size)
    current_node = start

    #While we isn't in the place where the value is zeros , run
    while grid[current_node] != 0:

        #Scann the neighbors, update the grid
        grid = scann_neigbhors(grid, current_node, size)

        #Then the grid updte chose a direction
        current_node =  chose_direction(grid, current_node, size)

        print('')
        print(current_node)
        print(grid)

main()
