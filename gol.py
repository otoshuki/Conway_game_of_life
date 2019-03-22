#Guining Pertin
#Conway's Game of Life using standard python library and numpy

#Import libraries
import numpy as np
import os
import json
import time

#Global variables
array_size_x = 0
array_size_y = 0

#Main
def main():
    #Initialize
    print("Welcome to Conway's Game of Life!")
    #Ask user for array size
    #Set as global variables
    global array_size_x
    global array_size_y
    #Create the empty array
    #array_size = user_input()
    array_size, delay = read_config()
    array_size_x = int(array_size[0])
    array_size_y = int(array_size[1])
    gol_array = np.zeros((array_size_y, array_size_x)).astype(int)
    #Show grid
    draw_grid(gol_array)
    print("\nGrid of size %d X %d initialized" %(array_size_x,array_size_y))
    gol_array = start_points(gol_array)
    #Play Game of Life
    print("Playing Game of Life")
    time.sleep(1)
    game_of_life(gol_array)

#Get user input for array dimensions
def user_input():
    print("Enter the array dimensions")
    #Ask until a proper answer
    while True:
        try:
            array_size = input("Enter array dimensions: ").split()
            #Check errors in data
            int(array_size[0])
            int(array_size[1])
            break
        except:
            print("Enter X and Y dimensions separated by whitespace")
    return array_size

#Basic grid
def draw_grid(array):
    os.system('cls' if os.name == 'nt' else 'clear')
    separator = "--- " * array_size_y
    for y in range(2*array_size_x):
        #For even rows - print hashes
        if y%2 == 0:
            print(separator)
        #For odd rows - print the character
        else:
            out = ' | '.join(map(str, array[int(y/2)]))
            out = ' ' + out
            out = out.replace('1', '#')
            out = out.replace('0', ' ')
            print(out)

#Get user_input for initial points
def start_points(array):
    while True:
        print("Select points to start off with(indexing at 1,1)")
        print("Enter done to complete")
        try:
            fill = input("Enter coordinates: ").split()
            #Check for exit
            if fill[0] == "done":
                print("Done")
                break
            fill_x = int(fill[0])
            fill_y = int(fill[1])
            if (fill_x > array_size_x) or (fill_y > array_size_y):
                print("Coordinates cannot be greater than array size")
                continue
            array[fill_y-1,fill_x-1] = 1
            draw_grid(array)
        except:
            print("Enter valid coordinates separated by whitespace")
    return array

#Conditions
def conditions(array_copy, changes, x, y):
    top = [y-1,x]
    bottom = [y+1,x]
    left = [y,x-1]
    right = [y,x+1]
    t_left = [y-1,x-1]
    t_right = [y-1,x+1]
    b_left = [y+1,x-1]
    b_right = [y+1,x+1]
    neighbours = [top, bottom, left, right, t_left, t_right, b_left, b_right]
    no_neighbours = 0
    #Check for number of neighbours
    for i, check in enumerate(neighbours):
        #If goes beyond upper limits
        if (check[0] >= array_size_x): check[0] = 0
        if (check[1] >= array_size_y): check[1] = 0
        #If goes beyond lower limit
        if (check[0] < 0): check[0] = array_size_x - 1
        if (check[1] < 0): check[1] = array_size_y - 1
        #Otherwise, check
        if array_copy[check[0],check[1]] == 1:
            no_neighbours += 1
    #Game of life conditions
    #1: live cell with less than two neighbours dies
    if (array_copy[y,x] == 1) and (no_neighbours < 2):
        changes[y,x] = 0
    #2: live cell with two or three neighbours lives, return same array
    if (array_copy[y,x] == 1) and (no_neighbours ==2 or no_neighbours == 3):
        return changes
    #3: live cell with more than three neighbours dies
    if (array_copy[y,x] == 1) and (no_neighbours > 3):
        changes[y,x] = 0
    #4: dead cell with exactly three live neighbours, becomes live
    if (array_copy[y,x] == 0) and (no_neighbours == 3):
        changes[y,x] = 1
    return changes

#Dump config
def dump_config(array_size, delay):
    config = {}
    config["array"] = []
    config["array"].append({
    "array_size_x" : array_size[0],
    "array_size_y" : array_size[1],
    })
    config["delay"] = []
    config["delay"].append({
    "delay" : delay,
    })
    print("Writing to config file")
    with open('config.json', 'w') as output:
        json.dump(config, output)

#Read config to json file
def read_config():
    config = {}
    with open("config.json") as config:
        file = json.load(config)
        for data in file["array"]:
            size_x = data["array_size_x"]
            size_y = data["array_size_y"]
        for data in file["delay"]:
            delay = data["delay"]
    print("Reading from config file")
    print("sizes : %s and %s" %(size_x, size_y))
    print("delay : %.2f" %(delay))
    return (size_x, size_y), delay

#The game of life
def game_of_life(array, delay = 0.1):
    iter = 0
    while True:
        changes = array.copy()
        time.sleep(delay)
        for x in range(array_size_x):
            for y in range(array_size_y):
                change = conditions(array.copy(), changes, x, y)
        array = change.copy()
        draw_grid(array)
        #Check if array is empty
        iter += 1
        print("Iteration : ", iter)
        if np.sum(array) == 0:
            break
    print("Ended")

#Run
if __name__ == "__main__":
    dump_config(user_input(), 0.05)
    main()
