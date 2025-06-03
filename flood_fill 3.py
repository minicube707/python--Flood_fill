import numpy as np

size = 5
grid = np.zeros((size, size), int)

grid_wall = np.zeros((size, size), int)
grid_wall[0, 1] = 1
grid_wall[1, 1] = 1
grid_wall[2, 1] = 1
grid_wall[3, 1] = 1


grid_wall[1, 3] = 1
grid_wall[2, 3] = 1
grid_wall[3, 3] = 1

grid_wall[1, 4] = 1

#Wall == -1
#END == 0

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


    #Left dir_val == 0
    if dir_val == 0:
        current_node = (current_node[0], current_node[1] - 1)

    #Right dir_val == 1
    elif dir_val == 1:
        current_node = (current_node[0], current_node[1] + 1)

    #Up dir_val == 2
    elif dir_val == 2:
        current_node = (current_node[0] - 1, current_node[1])
    
    #Down dir_val == 3
    else:
        current_node = (current_node[0] + 1, current_node[1])

    return current_node



def scann_neigbhors(grid, current_node, size):
    list_delta = [-1, 1]
    follow_path = False
    current_val = grid[current_node]

    #Update
    #Left Right
    for delta in list_delta:
        if 0 <= (current_node[1] + delta ) < size:
            if grid_wall[current_node[0], current_node[1] + delta] == 1:
                grid[current_node[0], current_node[1] + delta] = -1

            if grid[current_node[0], current_node[1] + delta] == current_val - 1:
                follow_path = True
            

    #Up Down
    for delta in list_delta:
        if 0 <= (current_node[0] + delta) < size:
            if grid_wall[current_node[0] + delta, current_node[1]] == 1:
                grid[current_node[0] + delta, current_node[1]] = -1

            if grid[current_node[0] + delta, current_node[1]] == current_val - 1:
                follow_path = True

    if not follow_path:
        grid = update_grid(grid, current_node)

    return grid



def update_grid(grid, current_node):
    list_delta = [-1, 1]
    list_neighbors = []
    list_neighbors.append(current_node)

    while len(list_neighbors) > 0:
        min_his = float("inf")
        node = list_neighbors[0]
        current_val = grid[node]

        #Left Right
        for delta in (list_delta):
            if 0 <= (node[1] + delta ) < size:
                if 0 < grid[node[0], node[1] + delta] < min_his:
                    min_his = grid[node[0], node[1] + delta]

    
        #Up Down
        for  delta in (list_delta):
            if 0 <= (node[0] + delta) < size:
                if 0 < grid[node[0] + delta, node[1]] < min_his:
                    min_his = grid[node[0] + delta, node[1] ]

        if min_his != current_val -1:
       
            
            grid[node] = (min_his +1)
            

            for delta in (list_delta):
                if 0 <= (node[1] + delta ) < size and grid[current_node[0], current_node[1] + delta] != -1:
                    neigbhors_node = (node[0], node[1] + delta)
                    list_neighbors.append(neigbhors_node)

                if 0 <= (node[0] + delta) < size and grid[current_node[0] + delta, current_node[1]] != -1:    
                    neigbhors_node = (node[0] + delta, node[1])
                    list_neighbors.append(neigbhors_node)

        list_neighbors.pop(0)
    return grid



def make_grid(grid, end):
    list_delta = [-1, 1]

    list_node = [end]

    while len(list_node) > 0:

        list_next_node = []

        for node in list_node:
            current_val = grid[node]

            for delta in list_delta:
                if 0 <= (node[0] + delta) < size:
                    if grid[node[0] + delta, node[1]] == 0:
                        grid[node[0] + delta, node[1]] = current_val + 1
                        list_next_node.append((node[0] + delta, node[1]))

            for delta in list_delta:
                if 0 <= (node[1] + delta ) < size:
                    if grid[node[0], node[1] + delta] == 0:
                        grid[node[0], node[1] + delta] = current_val + 1
                        list_next_node.append((node[0], node[1] + delta))


        list_node = []
        list_node = list_next_node 

    grid[end] = 0
     
    return grid


end = (0, 4)
start = (0, 0)
grid = make_grid(grid, end)
current_node = start

while grid[current_node] != 0:


    
    grid = scann_neigbhors(grid, current_node, size)
    current_node =  chose_direction(grid, current_node, size)
    print('')
    print(current_node)
    print(grid)


    