import numpy as np

size = 5
grid = np.zeros((size, size), int)
grid[2, 2] = -1
grid[1, 2] = -1
grid[0, 2] = -1

#Wall == -1
#END == 0



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
grid = make_grid(grid, end)

print(grid)
