# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:24:05 2024

@author: 15105
"""

import numpy as np
import matplotlib.pyplot as plt

# Define grid size and initialize the grid
grid_size = 30
grid = np.zeros((grid_size, grid_size))

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

# Initialize gradient rings
gradient_values = np.zeros((grid_size, grid_size))
target_x, target_y = np.random.randint(0, grid_size, size=2)
for r in [0.1, 0.4, 0.7]:
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            nx, ny = target_x + dx, target_y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                distance = np.sqrt((target_x - nx)**2 + (target_y - ny)**2)
                if distance <= 2:  # Modify the range as desired
                    gradient_values[nx, ny] = max(gradient_values[nx, ny], r + 0.2 * (2 - distance))

# Function to update the UAV positions
def update_uav_positions():
    global perimeter_positions, grid, gradient_values

    for i in range(num_uavs):
        x, y = perimeter_positions[i]
        
        # Save the current position of the UAV
        uav_locations[i].append((x, y))
        
        # Check if the UAV found the target based on gradient values
        if gradient_values[x, y] > 0:
            # Move towards increasing values in the gradient
            max_value = -1
            best_move = None
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            np.random.shuffle(moves)
            for move in moves:
                new_x, new_y = x + move[0], y + move[1]
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    if gradient_values[new_x, new_y] > max_value:
                        max_value = gradient_values[new_x, new_y]
                        best_move = move
            
            if best_move:
                new_x, new_y = x + best_move[0], y + best_move[1]
                perimeter_positions[i] = [new_x, new_y]
        else:
            # Move randomly if not in a gradient zone
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            np.random.shuffle(moves)
            for move in moves:
                new_x, new_y = x + move[0], y + move[1]
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                    perimeter_positions[i] = [new_x, new_y]
                    break
        
        # Check if the UAV found the target
        if gradient_values[x, y] > 0:
            return True, i
        
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

# Plot the entire path taken by the UAV that finds the person with gradient visualization
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav])

    plt.figure(figsize=(12, 8), facecolor='white')

    # Plot the gradient values
    plt.imshow(gradient_values, cmap='viridis', origin='lower', extent=[0, grid_size, 0, grid_size])
    
    # Plot the path taken by the UAV
    plt.plot(path_y, path_x, marker='o', linestyle='-', color='b', label='UAV Path')
    
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

# Plot only the last few steps taken by the UAV that finds the person with a zoomed-in view
if found_uav is not None:
    path_x, path_y = zip(*uav_locations[found_uav])
    last_steps = 5  # Define the number of last steps to plot
    last_path_x, last_path_y = path_x[-last_steps:], path_y[-last_steps:]
    
    plt.figure(figsize=(12, 8))
    
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
