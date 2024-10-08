#Description: Demonstrating navigating out of a simple maze using the left-hand method.
#Author: souXess
#Created: 17Sep2024
#Last Modified: 17Sep2024

import time

Map = [['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
       ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
       ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
       ['X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X'],
       ['X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
       ['X', 'X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X'],
       ['X', ' ', ' ', 'X', ' ', 'X', 'X', ' ', 'X', 'X', ' ', 'X'],
       ['X', 'X', 'X', 'X', ' ', 'X', 'X', ' ', ' ', 'X', ' ', 'X'],
       ['X', 'X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
       ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
       ['X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
       ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'S', 'X']]

LocationTracker = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


#Find the start position 'S' on the map
def find_start_position():
    for i, lst in enumerate(Map):
        for j, l in enumerate(lst):
            if l == 'S':
                return [i, j]
    return [None, None]

def print_status():
    print('\nCave Crawler 1.0\n')
    #If back at the start position
    if Route.count(find_start_position()) > 1:
        print('Oops! Looks like we\'ve come back to where we started. Let\'s turn around.\n')
    #At the starting position
    elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
        print('Welcome to Cave Crawler 1.0! Let\'s see if we can find our way out of this cave.\n')
    #Reached the end
    elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
        print('Yay! We\'ve found our way out of the cave.\n') 
    print(f'Current Direction: {Direction}\n' +
          f'Current Position: {CurrentPosition}\n' +
          f'Previous Position: {PreviousPosition}\n' +
          f'Distance Travelled: {DistanceTravelled} m\n' +
          f'Route: {Route}')
    print(*LocationTracker, '\n', sep='\n')
    print(*Map, sep='\n')

#Set the initial current position as the start position
CurrentPosition = find_start_position()

PreviousPosition = []

#Append the initial start position to the route
Route = []
Route.append(CurrentPosition)

#Set initial direction to forward
Direction = 'Forward'

DistanceTravelled = 0

#Insert an '@' at the start position on the location tracker
LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'

print_status()

#Pause for effect
time.sleep(3)

while Map[CurrentPosition[0]][CurrentPosition[1]] != 'E':
    #Movement Key:
    #Move forward = Map[CurrentPosition[0] - 1][CurrentPosition[1]]
    #Move backward = Map[CurrentPosition[0] + 1][CurrentPosition[1]]
    #Move left = Map[CurrentPosition[0]][CurrentPosition[1] - 1]
    #Move right = Map[CurrentPosition[0]][CurrentPosition[1] + 1]
    
    #Moving forward
    while Direction == 'Forward':
        #If there is a wall to the left and no wall forward, go forward
        if (Map[CurrentPosition[0]][CurrentPosition[1] - 1] == 'X' 
            and Map[CurrentPosition[0] - 1][CurrentPosition[1]] != 'X'):
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] - 1] = 'W'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0] - 1, CurrentPosition[1]]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Backward'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
        #If there is no wall to the left, turn left
        elif Map[CurrentPosition[0]][CurrentPosition[1] - 1] != 'X':
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0], CurrentPosition[1] - 1]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            Direction = 'Left'
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Backward'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
            break
        #If a deadend is reached
        else:
            LocationTracker[CurrentPosition[0] - 1][CurrentPosition[1]] = 'W'
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] - 1] = 'W'
            Direction = 'Backward'
            print_status()
            time.sleep(3)
            
    #Moving left
    while Direction == 'Left':
        #If there is a wall to the left (Backward position), go forward (Left direction)
        if (Map[CurrentPosition[0] + 1][CurrentPosition[1]] == 'X'
            and Map[CurrentPosition[0]][CurrentPosition[1] - 1] != 'X'):
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            LocationTracker[CurrentPosition[0] + 1][CurrentPosition[1]] = 'W'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0], CurrentPosition[1] - 1]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Right'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
        #If there is no wall to the left (Backward position), turn left (Backward direction)
        elif Map[CurrentPosition[0] + 1][CurrentPosition[1]] != 'X':
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0] + 1, CurrentPosition[1]]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            Direction = 'Backward'
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Right'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
            break
        #If a deadend is reached, turn around
        else:
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] - 1] = 'W'
            LocationTracker[CurrentPosition[0] + 1][CurrentPosition[1]] = 'W'
            Direction = 'Right'
            print_status()
            time.sleep(3)
        
    #Moving right
    while Direction == 'Right':
        #If there is a wall to the left (forward position), go forward (right direction)
        if (Map[CurrentPosition[0] - 1][CurrentPosition[1]] == 'X'
            and Map[CurrentPosition[0]][CurrentPosition[1] + 1] != 'X'):
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            LocationTracker[CurrentPosition[0] - 1][CurrentPosition[1]] = 'W'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0], CurrentPosition[1] + 1]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Left'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
        #If there is no wall to the left (forward position), turn left (forward direction)
        elif Map[CurrentPosition[0] - 1][CurrentPosition[1]] != 'X':
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0] - 1, CurrentPosition[1]]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            Direction = 'Forward'
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Left'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
            break
        #If a deadend is reached, turn around
        else:
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] + 1] = 'W'
            LocationTracker[CurrentPosition[0] - 1][CurrentPosition[1]] = 'W'
            Direction = 'Left'
            print_status()
            time.sleep(3)
        
    #Moving backward
    while Direction == 'Backward':
        #If there is a wall to the left (right position) and no wall forward (backward direction), go forward (backward position)
        if (Map[CurrentPosition[0]][CurrentPosition[1] + 1] == 'X' 
            and Map[CurrentPosition[0] + 1][CurrentPosition[1]] != 'X'):
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] + 1] = 'W'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0] + 1, CurrentPosition[1]]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Forward'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
        #If there is no wall to the left (right position), turn left (right direction)
        elif Map[CurrentPosition[0]][CurrentPosition[1] + 1] != 'X':
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '*'
            PreviousPosition = CurrentPosition
            CurrentPosition = [CurrentPosition[0], CurrentPosition[1] + 1]
            LocationTracker[CurrentPosition[0]][CurrentPosition[1]] = '@'
            Route.append(CurrentPosition)
            Direction = 'Right'
            DistanceTravelled += 10
            #If the exit has been reached
            if Map[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                print_status()
                break
            #If back at the start position
            elif Map[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                Direction = 'Forward'
                print_status()
                time.sleep(3)
                break
            print_status()
            time.sleep(3)
            break
        #If a deadend is reached, turn around
        else:
            LocationTracker[CurrentPosition[0] + 1][CurrentPosition[1]] = 'W'
            LocationTracker[CurrentPosition[0]][CurrentPosition[1] + 1] = 'W'
            Direction = 'Forward'
            print_status()
            time.sleep(3)    
