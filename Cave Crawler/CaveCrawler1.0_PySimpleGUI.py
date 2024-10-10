#Description: A simple program that implements the left-hand search method for finding a way out of a simple maze (or cave).
#Author: souXess
#Created: 10Oct2024
#Last Modified: 10Oct2024

import PySimpleGUI as sg
import threading as t
import time 

"""
CaveTemplate = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]
"""

BlankGrid = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
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

Cave1 = [['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
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

Cave2 = [['X', 'X', 'X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'S', 'X'],
         ['X', 'X', 'X', ' ', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
         ['X', 'X', 'X', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
         ['X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X'],
         ['X', ' ', ' ', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X'],
         ['X', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', ' ', 'X', 'X'],
         ['X', ' ', 'X', 'X', ' ', 'X', 'X', 'X', 'X', ' ', 'X', 'X'],
         ['X', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', ' ', 'X', 'X'],
         ['X', 'X', ' ', 'X', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X'],
         ['X', 'X', ' ', 'X', ' ', 'X', 'X', ' ', 'X', 'X', 'X', 'X'],
         ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'X'],
         ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

Cave3 = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'E'],
         ['X', ' ', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X'],
         ['X', ' ', ' ', ' ', 'X', 'X', 'X', 'X', ' ', ' ', ' ', 'X'],
         ['X', 'X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
         ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', 'X'],
         ['X', ' ', 'X', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X'],
         ['X', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
         ['X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X'],
         ['S', ' ', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
         ['X', ' ', ' ', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

Cave4 = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'E', 'X', 'X'],
         ['X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
         ['X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X', ' ', 'X'],
         ['X', 'X', 'X', 'X', ' ', ' ', 'X', ' ', 'X', 'X', ' ', 'X'],
         ['X', ' ', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' ', ' ', 'X'],
         ['X', 'X', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
         ['X', 'X', ' ', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
         ['X', 'X', ' ', ' ', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X'],
         ['X', ' ', 'X', 'X', ' ', 'X', ' ', 'X', 'X', 'X', 'X', 'X'],
         ['X', ' ', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'S'],
         ['X', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

Cave5 = [['X', 'E', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
         ['X', 'X', ' ', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', 'X'],
         ['X', 'X', ' ', 'X', 'X', ' ', 'X', ' ', ' ', ' ', ' ', 'X'],
         ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', 'X', 'X', ' ', 'X'],
         ['X', 'X', 'X', 'X', ' ', 'X', 'X', ' ', 'X', ' ', ' ', 'X'],
         ['X', ' ', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X'],
         ['X', ' ', 'X', 'X', ' ', 'X', 'X', ' ', 'X', ' ', ' ', 'X'],
         ['X', ' ', ' ', 'X', ' ', 'X', 'X', ' ', 'X', ' ', 'X', 'X'],
         ['X', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
         ['X', ' ', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
         ['X', 'S', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

#Find the start position 'S' in the cave
def find_start_position(cave):
    for i, lst in enumerate(cave):
        for j, l in enumerate(lst):
            if l == 'S':
                return [i, j]

CaveList = ['Select Cave...', 'Cave 1', 'Cave 2', 'Cave 3', 'Cave 4', 'Cave 5']
CurrentPosition = ''
PreviousPosition = ''
Route = ''
Direction = ''
TotalMeters = 0
SearchPaused = False
Cave = ''
Message = 'Welcome to Cave Crawler!\nPlease select a cave and let\'s see if we can find our way out of it.'

"""
#No longer necessary
#Generate the Cave and Route Mapper button grids
def create_button_grid(index, cave):
        def get_value():
            for lst in cave:
                for v in lst:
                    yield v
        gen = get_value()
        return [[sg.Button(next(gen) if index == 0 else '', size = (2, 1), pad = (0, 0), disabled = True, 
                 disabled_button_color = ('#FFFFFF', None),
                 key = (index, row, col)) for col in range(12)] for row in range(12)]
 """

#Generate the Cave and Route Mapper button grids    
def create_button_grid(index):
    return [[sg.Button('', size=(2, 1), pad = (0, 0), disabled = True, disabled_button_color = ('#FFFFFF', None), 
             key = (index, row, col)) for col in range(12)] for row in range(12)]

layout = [[sg.Push(), sg.Text(Message, font = (None, 12), colors = '#90EE90', justification = 'center', 
           size = (None, 2), key = '-MESSAGE-'), sg.Push()],
          [sg.Text('Current Direction:'), sg.Text('', key = '-DIRECTION-')],
          [sg.Text('Current Position:'), sg.Text('', key = '-CURRENTPOSITION-')],
          [sg.Text('Previous Position:'), sg.Text('', key = '-PREVIOUSPOSITION-')],
          [sg.Text('Distance Travelled:'), sg.Text('', key = '-TOTALMETERS-')],
          [sg.Text('Route:'), sg.Multiline('', autoscroll = True, disabled = True, expand_y = True, expand_x = True,
           background_color = '#64778d', text_color = '#ffffff', key = '-ROUTE-')],
          [sg.Frame('No Cave Selected', create_button_grid(0), key = '-CAVEMAP-'), sg.VerticalSeparator(), 
           sg.Frame('Route Mapper', create_button_grid(1))],
          [sg.Text('Cave:'), sg.Listbox(values = CaveList, enable_events = True, 
           background_color = '#64778d', text_color = '#ffffff', expand_y = True, key = '-CAVELIST-' ), 
           sg.Button('Start', disabled = True, key = '-START-'),
           sg.Button('Pause', disabled = True, key = '-PAUSE-'),
           sg.Button('Reset', disabled = True, key = '-RESET-')]]

window = sg.Window('Cave Crawler 1.0', layout, finalize = True)

window['-START-'].set_cursor('hand2')
window['-RESET-'].set_cursor('hand2')
window['-CAVELIST-'].set_cursor('hand2')
window['-PAUSE-'].set_cursor('hand2')

while True:
    event, values = window.read()
    
    def refresh_window(msg):
        if msg == 0:
            window['-MESSAGE-'].update('Searching for a way out...')
        elif msg == 1:
            window['-MESSAGE-'].update('Yay! We\'ve found our way out of the cave.')
        elif msg == 2:
            window['-MESSAGE-'].update('Oops. Looks like we\'ve come back to where we started. Let\'s turn around.')
        elif msg == 3:
            window['-MESSAGE-'].update('There\'s a wall in front of us. Let\'s turn around.')
            
        if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
            window['-RESET-'].update(disabled = False)
            window['-PAUSE-'].update(disabled = True)
        
        window['-DIRECTION-'].update(Direction)
        window['-CURRENTPOSITION-'].update(CurrentPosition)
        window['-PREVIOUSPOSITION-'].update(PreviousPosition)
        window['-TOTALMETERS-'].update(f'{TotalMeters} m')
        window['-ROUTE-'].update(Route)
        window.refresh()
    
    def draw_cave(cave):
        if cave == ['Select Cave...']:
            cave = BlankGrid
            window['-CAVEMAP-'].update('No Cave Selected')
        elif cave == ['Cave 1']:
            cave = Cave1
            window['-CAVEMAP-'].update('Cave 1')
        elif cave == ['Cave 2']:
            cave = Cave2
            window['-CAVEMAP-'].update('Cave 2')
        elif cave == ['Cave 3']:
            cave = Cave3
            window['-CAVEMAP-'].update('Cave 3')
        elif cave == ['Cave 4']:
            cave = Cave4
            window['-CAVEMAP-'].update('Cave 4')
        elif cave == ['Cave 5']:
            cave = Cave5
            window['-CAVEMAP-'].update('Cave 5')
                            
        for i, lst in enumerate(cave):
                for j, l in enumerate(lst):
                    if l == 'S' or l == 'E': 
                        window[(0, i, j)].update(disabled_button_color = ('#90EE90', None))
                    else:
                        window[(0, i, j)].update(disabled_button_color = ('#ffffff', None))
                        
                    window[(0, i, j)].update(l)
        
        if cave != BlankGrid:
            window['-START-'].update(disabled = False)
        else:
            window['-START-'].update(disabled = True)
            
        window.refresh()
           
    def search_cave():
        global CurrentPosition, PreviousPosition, Route, Direction, TotalMeters, Cave 
                
        while Cave[CurrentPosition[0]][CurrentPosition[1]] != 'E':
            if event == '-PAUSE-':
                break
            
            #Movement Key:
            #Forward = window[1, CurrentPosition[0] - 1, CurrentPosition[1]]
            #Backward = window[1, CurrentPosition[0] + 1, CurrentPosition[1]]
            #Left = window[1, CurrentPosition[0], CurrentPosition[1] - 1]
            #Right = window[1, CurrentPosition[0], CurrentPosition[1] + 1]
            
            #Moving forward
            while Direction == 'Forward':
                if event == '-PAUSE-':
                    break
                 #If there is a wall to the left and no wall forward, go forward
                if (Cave[CurrentPosition[0]][CurrentPosition[1] - 1] == 'X' 
                    and Cave[CurrentPosition[0] - 1][CurrentPosition[1]] != 'X'):
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    window[(1, CurrentPosition[0], CurrentPosition[1] - 1)].update('W')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0] - 1, CurrentPosition[1]]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Backward'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                #If there is no wall to the left, turn left
                elif Cave[CurrentPosition[0]][CurrentPosition[1] - 1] != 'X':
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0], CurrentPosition[1] - 1]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    Direction = 'Left'
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Backward'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                    break
                #If there is a wall forward
                else:
                    window[(1, CurrentPosition[0] - 1, CurrentPosition[1])].update('W')
                    window[(1, CurrentPosition[0], CurrentPosition[1] - 1)].update('W')
                    Direction = 'Backward'
                    refresh_window(3)
                    time.sleep(1.5)
                   
            #Moving left
            while Direction == 'Left':
                if event == '-PAUSE-':
                    break
                #If there is a wall to the left (Backward position), go forward (Left direction)
                if (Cave[CurrentPosition[0] + 1][CurrentPosition[1]] == 'X'
                    and Cave[CurrentPosition[0]][CurrentPosition[1] - 1] != 'X'):
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    window[(1, CurrentPosition[0] + 1, CurrentPosition[1])].update('W')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0], CurrentPosition[1] - 1]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(0)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Right'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                #If there is no wall to the left (Backward position), turn left (Backward direction)
                elif Cave[CurrentPosition[0] + 1][CurrentPosition[1]] != 'X':
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0] + 1, CurrentPosition[1]]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    Direction = 'Backward'
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(0)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Right'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                    break
                #If there is a wall forward (left direction)
                else:
                    window[(1, CurrentPosition[0], CurrentPosition[1] - 1)].update('W')
                    window[(1, CurrentPosition[0] + 1, CurrentPosition[1])].update('W')
                    Direction = 'Right'
                    refresh_window(3)
                    time.sleep(1.5)

            #Moving right
            while Direction == 'Right':
                if event == '-PAUSE-':
                    break
                #If there is a wall to the left (forward position), go forward (right direction)
                if (Cave[CurrentPosition[0] - 1][CurrentPosition[1]] == 'X'
                    and Cave[CurrentPosition[0]][CurrentPosition[1] + 1] != 'X'):
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    window[(1, CurrentPosition[0] - 1, CurrentPosition[1])].update('W')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0], CurrentPosition[1] + 1]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Left'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                #If there is no wall to the left (forward position), turn left (forward direction)
                elif Cave[CurrentPosition[0] - 1][CurrentPosition[1]] != 'X':
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0] - 1, CurrentPosition[1]]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    Direction = 'Forward'
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Left'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                    break
                #If there is a wall forward (right direction)
                else:
                    window[(1, CurrentPosition[0], CurrentPosition[1] + 1)].update('W')
                    window[(1, CurrentPosition[0] - 1, CurrentPosition[1])].update('W')
                    Direction = 'Left'
                    refresh_window(3)
                    time.sleep(1.5)
                    
            #Moving backward
            while Direction == 'Backward':
                if event == '-PAUSE-':
                    break
                #If there is a wall to the left (right position) and no wall forward (backward direction), go forward (backward position)
                if (Cave[CurrentPosition[0]][CurrentPosition[1] + 1] == 'X' 
                    and Cave[CurrentPosition[0] + 1][CurrentPosition[1]] != 'X'):
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    window[(1, CurrentPosition[0], CurrentPosition[1] + 1)].update('W')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0] + 1, CurrentPosition[1]]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Forward'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                #If there is no wall to the left (right position), turn left (right direction)
                elif Cave[CurrentPosition[0]][CurrentPosition[1] + 1] != 'X':
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('*')
                    PreviousPosition = CurrentPosition
                    CurrentPosition = [CurrentPosition[0], CurrentPosition[1] + 1]
                    window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')
                    Route.append(CurrentPosition)
                    Direction = 'Right'
                    TotalMeters += 10
                    #If the exit has been reached
                    if Cave[CurrentPosition[0]][CurrentPosition[1]] == 'E':
                        refresh_window(1)
                        break
                    #If back at the start position
                    elif Cave[CurrentPosition[0]][CurrentPosition[1]] == 'S':
                        Direction = 'Forward'
                        refresh_window(2)
                        time.sleep(1.5)
                        break
                    refresh_window(0)
                    time.sleep(1.5)
                    break
                #If there is a wall forward (backward direction)
                else:
                    window[(1, CurrentPosition[0] + 1, CurrentPosition[1])].update('W')
                    window[(1, CurrentPosition[0], CurrentPosition[1] + 1)].update('W')
                    Direction = 'Forward'
                    refresh_window(3)
                    time.sleep(1.5)    
        
    if event == sg.WIN_CLOSED:
        break
    elif event == '-RESET-':
        for i, lst in enumerate(BlankGrid):
                for j, l in enumerate(lst):
                    window[(0, i, j)].update(disabled_button_color = ('#ffffff', None))
                    window[(1, i, j)].update(disabled_button_color = ('#ffffff', None))
                    window[(0, i, j)].update(l)
                    window[(1, i, j)].update(l)
                    
        CurrentPosition = ''
        PreviousPosition = ''
        Route = ''
        Direction = ''
        TotalMeters = 0
        SearchPaused = False
        Cave = ''
        
        window['-CAVEMAP-'].update('No Cave Selected')
        window['-DIRECTION-'].update('')
        window['-CURRENTPOSITION-'].update('')
        window['-PREVIOUSPOSITION-'].update('')
        window['-TOTALMETERS-'].update('')
        window['-ROUTE-'].update('')
        window['-RESET-'].update(disabled = True)
        window['-START-'].update(disabled = True)
        window['-PAUSE-'].update(disabled = True)
        window['-CAVELIST-'].update(disabled = False)
        window['-MESSAGE-'].update('Please select a cave to play again.')
        window.refresh()
    elif event == '-CAVELIST-':
        draw_cave(values.get('-CAVELIST-'))
    elif event == '-PAUSE-':
        SearchPaused = True
        window['-MESSAGE-'].update('Search Paused.')
        window['-PAUSE-'].update(disabled = True)
        window['-START-'].update(disabled = False)
        window['-RESET-'].update(disabled = False)
        window.refresh()
    elif event == '-START-':
        if SearchPaused == False:
            if values.get('-CAVELIST-') == ['Cave 1']:
                Cave = Cave1
                Direction = 'Forward'
            elif values.get('-CAVELIST-') == ['Cave 2']:
                Cave = Cave2
                Direction = 'Backward'
            elif values.get('-CAVELIST-') == ['Cave 3']:
                Cave = Cave3
                Direction = 'Right'
            elif values.get('-CAVELIST-') == ['Cave 4']:
                Cave = Cave4
                Direction = 'Left'
            elif values.get('-CAVELIST-') == ['Cave 5']:
                Cave = Cave5
                Direction = 'Forward'

            CurrentPosition = find_start_position(Cave)
            Route = [[CurrentPosition[0], CurrentPosition[1]]]

            window['-DIRECTION-'].update(Direction)
            window['-CURRENTPOSITION-'].update(CurrentPosition)
            window['-ROUTE-'].update(Route)

            window[(1, CurrentPosition[0], CurrentPosition[1])].update('@')

            window['-MESSAGE-'].update('Searching for a way out...')
            window.refresh()
            time.sleep(1.5)
        
        SearchPaused = False
        window['-START-'].update(disabled = True)
        window['-CAVELIST-'].update(disabled = True)
        window['-RESET-'].update(disabled = True)
        window['-PAUSE-'].update(disabled = False)
        
        t1 = t.Thread(target = search_cave)
        t1.start()
        
window.close()