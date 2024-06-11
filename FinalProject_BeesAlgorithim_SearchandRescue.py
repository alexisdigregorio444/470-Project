import numpy as np
import matplotlib.pyplot as plt

# Define grid size and initialize the grid
grid_size = 30
grid = np.zeros((grid_size, grid_size))

# Define the truth grid with only the location of the person marked
truth_grid = np.zeros((grid_size, grid_size))

# Place the person to be rescued at a random location
target_x, target_y = np.random.randint(0, grid_size, size=2)
truth_grid[target_x, target_y] = 1

print(f"Target located at: ({target_x}, {target_y})")

# Display the truth grid matrix
# print("Truth Grid Matrix:")
print(truth_grid)

# Initialize UAV positions evenly along the perimeter
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

perimeter_positions = perimeter_positions[:num_uavs]

# Save the locations of the UAVs
uav_locations = {i: [] for i in range(num_uavs)}

# Function to update the UAV positions
def update_uav_positions():
    global perimeter_positions, grid, truth_grid

    for i in range(num_uavs):
        x, y = perimeter_positions[i]
        
        # Save the current position of the UAV
        uav_locations[i].append((x, y))
        
        # Check if the UAV found the target in the truth grid
        if truth_grid[x, y] == 1:
            return True, i
        
        # Update the grid with decreasing values around the target
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    distance = np.sqrt((target_x - nx)**2 + (target_y - ny)**2)
                    if distance <= 2:  # Modify the range as desired
                        grid[nx, ny] = max(grid[nx, ny], 0.2 + 0.2 * (2 - distance))

        # Choose a new direction to move
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        np.random.shuffle(moves)
        
        for move in moves:
            new_x, new_y = x + move[0], y + move[1]
            if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                perimeter_positions[i] = [new_x, new_y]
                break
        
    return False, None

# Function to move all other UAVs to the position of the found UAV
def move_other_uavs(found_uav_index):
    global perimeter_positions
    found_uav_position = perimeter_positions[found_uav_index]
    for i in range(num_uavs):
        if i != found_uav_index:
            perimeter_positions[i] = found_uav_position


# Define a list to store the positions of all UAVs at each step
all_uavs_positions = []

import matplotlib.cm as cm

# Define a list of colors for each UAV
colors = cm.rainbow(np.linspace(0, 1, num_uavs))

# Main loop
found = False
found_uav = None
steps = 0
while not found:
    # Append the current positions of all UAVs
    all_uavs_positions.append(perimeter_positions.copy())
    
    found, found_uav = update_uav_positions()
    steps += 1

if found:
    print(f"Person found in {steps} steps by UAV {found_uav} at: ({perimeter_positions[found_uav][0]}, {perimeter_positions[found_uav][1]})")
    move_other_uavs(found_uav)  # Move other UAVs to the position of the found UAV
else:
    print("Person not found within the grid.")

# Plot the entire path taken by the UAV that finds the person
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav])
    plt.figure(figsize=(8, 8), facecolor='white')  # Set the size and facecolor of the figure
    
    # Plot the grid
    #plt.imshow(grid, cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)
    
    # Plot the path taken by the UAV
    plt.plot(path_y, path_x, marker='o', linestyle='-', color='b')
    
    # Plot the target and starting location
    plt.plot(target_y, target_x, marker='x', color='r', markersize=10, label='Target')
    start_x, start_y = uav_locations[found_uav][0]
    plt.plot(start_y, start_x, marker='s', color='g', markersize=10, label='Start')
    
    plt.title(f"Path taken by UAV {found_uav} to find the person")
    plt.xlabel("Column")
    plt.ylabel("Row")
    plt.xlim(0, grid_size)  # Set x-axis limit from 0 to grid_size
    plt.ylim(0, grid_size)  # Set y-axis limit from 0 to grid_size
    plt.gca().set_aspect('equal', adjustable='box')  # Set equal aspect ratio
    plt.legend()
    plt.grid(True)
    plt.show()


# Plot only the last few steps taken by the UAV that finds the person with a zoomed-in view
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav])
    last_steps = 5  # Define the number of last steps to plot
    last_path_x, last_path_y = path_x[-last_steps:], path_y[-last_steps:]
    
    plt.figure(figsize=(8, 8))
    
    # Plot the white background
    plt.imshow(np.ones_like(grid), cmap='gray', origin='lower', extent=[0, grid_size, 0, grid_size], vmin=0, vmax=1)
    
    # Plot the path taken by the UAV (last few steps)
    plt.plot(last_path_y, last_path_x, marker='o', linestyle='-', color='b', label=f'Last {last_steps} steps')
    plt.plot(target_y, target_x, marker='x', color='r', markersize=10, label='Target')
    # Mark the starting location of the UAV with a different marker
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


