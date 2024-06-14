
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# bees algorithm for finding the crash site --> search and rescue mission 


# Define grid as a 30 by 30 and initialize the grid
grid_size = 30
grid = np.zeros((grid_size, grid_size))

# create initial UAV positions - evenly space along the perimeter (// incase the spacing isnt integer)
num_uavs = 10
perimeter_positions = []
# Top and bottom rows
for i in range(num_uavs // 2): 
    perimeter_positions.append([0, i * (grid_size - 1) // (num_uavs // 2 - 1)])
    perimeter_positions.append([grid_size - 1, i * (grid_size - 1) // (num_uavs // 2 - 1)])

# Left and right columns (excluding corners)
for i in range(num_uavs - num_uavs // 2):
    perimeter_positions.append([i * (grid_size - 1) // (num_uavs - num_uavs // 2 - 1), 0])
    perimeter_positions.append([i * (grid_size - 1) // (num_uavs - num_uavs // 2 - 1), grid_size - 1])

# all positions up to num of UAVs
perimeter_positions = perimeter_positions[:num_uavs]

# create a dictionary saaaving locations of all the UAVs
uav_locations = {i: [] for i in range(num_uavs)}

# generate gradient for search space- size of grid 
gradient_values = np.zeros((grid_size, grid_size))
target_x, target_y = np.random.randint(0, grid_size, size=2)
for r in [0.1, 0.4, 0.7]: # numbers surnounding 1 for gradient 
    for dx in range(-2, 3): # x pos range
        for dy in range(-2, 3): # y pos range
            nx, ny = target_x + dx, target_y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                distance = np.sqrt((target_x - nx)**2 + (target_y - ny)**2)
                if distance <= 2:  # can change the range if wanted 
                    gradient_values[nx, ny] = max(gradient_values[nx, ny], r + 0.2 * (2 - distance)) # generate gradient 

# Function to update position of UAV
def update_uav_positions():
    global perimeter_positions, grid, gradient_values # set globasl

    for i in range(num_uavs): # for each UAV go throgh 
        x, y = perimeter_positions[i]
        
        # Save the current pos of the UAV
        uav_locations[i].append((x, y))
        
        # did the UAV find the crash site based on the grid value?
        if gradient_values[x, y] > 0:
            # move towards increasing values in the gradient
            max_value = -1
            best_move = None
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            np.random.shuffle(moves)
            # move --> 
            for move in moves:
                new_x, new_y = x + move[0], y + move[1]
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    # if gradient value is new max value- reset mac value --> feedback 
                    if gradient_values[new_x, new_y] > max_value:
                        max_value = gradient_values[new_x, new_y]
                        best_move = move
            
            if best_move:
                new_x, new_y = x + best_move[0], y + best_move[1]
                perimeter_positions[i] = [new_x, new_y]
        else:
            # move the UAVs randomly if not in a gradient zone
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            np.random.shuffle(moves)
            for move in moves:
                new_x, new_y = x + move[0], y + move[1]
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    perimeter_positions[i] = [new_x, new_y]
                    break
        
        # Did the UAV find its target ?
        if gradient_values[x, y] > 0:
            return True, i
        
    return False, None

# Move all other UAVs to the position of the UAV that found the crash site
def move_other_uavs(found_uav_index):
    global perimeter_positions # set global 
    found_uav_position = perimeter_positions[found_uav_index]
    for i in range(num_uavs):
        if i != found_uav_index:
            perimeter_positions[i] = found_uav_position

# list to store pos of each UAV
all_uavs_positions = []

# Define a list of colors for each UAV - for plotting 
colors = cm.rainbow(np.linspace(0, 1, num_uavs)) # yay rainbwo (:

# Loop thorugh 
found = False
found_uav = None
steps = 0
while not found:
    all_uavs_positions.append(perimeter_positions.copy())  # append all UAv cucrent positon
    
    found, found_uav = update_uav_positions()
    steps += 1

# if found
if found: # how many setps, which UAV --> print
    print(f"Person found in {steps} steps by UAV {found_uav} at: ({perimeter_positions[found_uav][0]}, {perimeter_positions[found_uav][1]})")
    move_other_uavs(found_uav)  # Move other UAVs to the position of the found UAV
else: # otherwise say not found 
    print("Person not found within the grid.")

# plot the entire path taken by the given UAV with gradient system
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav]) # zip together 

    # plot
    plt.figure(figsize=(12, 8), facecolor='white')
    plt.imshow(gradient_values, cmap='viridis', origin='lower', extent=[0, grid_size, 0, grid_size])  # Plot the gradient values
    plt.plot(path_y, path_x, marker='o', linestyle='-', color='b', label='UAV Path') # Plot the path taken by the UAV
    
    # Plot the target and starting location
    plt.plot(target_y, target_x, marker='x', color='r', markersize=10, label='Target')
    start_x, start_y = uav_locations[found_uav][0]
    plt.plot(start_y, start_x, marker='s', color='g', markersize=10, label='Start')
    
    plt.title(f"Path taken by UAV {found_uav} to find the person")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.colorbar(label='Gradient Value')
    plt.grid(True)
    plt.show()

# Plot only the last few steps taken by the UAV that finds the person with a zoomed-in view - for a better visualization 
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav])
    last_steps = 5 #dfefine the number of last steps to plot
    last_path_x, last_path_y = path_x[-last_steps:], path_y[-last_steps:]
    
    # plot the fig
    plt.figure(figsize=(12, 8))
    plt.imshow(np.ones_like(grid), cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1) # amke background nice 
    plt.plot(last_path_y, last_path_x, marker='o', linestyle='-', color='b', label=f'Last {last_steps} steps') # plot the last few steps 
    plt.plot(target_y, target_x, marker='x', color='r', markersize=10, label='Target')
    start_x, start_y = uav_locations[found_uav][0]
    plt.plot(start_y, start_x, marker='s', color='g', markersize=10, label='Start')
    
    plt.title(f"Last steps taken by UAV {found_uav}")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.xlim(min(last_path_y) - 2, max(last_path_y) + 2)
    plt.ylim(min(last_path_x) - 2, max(last_path_x) + 2)
    plt.legend()
    plt.grid(True)
    plt.show()
