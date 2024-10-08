#Description: Figuring out how to programmatically import values from a list of lists to the corresponding buttons in a grid.
#Author: souXess
#Created: 27Sep2024
#Last Modified: 27Sep2024

import PySimpleGUI as sg

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

"""
#Receive an error about using an element more than once in a layout
def create_button_grid(index):
    ButtonGrid = []
    MaxCols = MaxRows = 12
    for i, lst in enumerate(xlist):
        for j, v in enumerate(lst):
            ButtonGrid.append([sg.Button(v, size=(2, 1), pad = (0, 0), key = (index, i, j))])
    return [ButtonGrid for col in range(MaxCols) for row in range(MaxRows)]

#Populates only the first button with the first item (0,0) from Map
def create_button_grid(index):
    MaxCols = MaxRows = 12
    for lst in xlist:
        for v in lst:
            return [[sg.Button(v, size=(2, 1), pad = (0, 0), key = (index, row, col)) 
                     for col in range(MaxCols)] for row in range(MaxRows)]
                     
#Creates grid of buttons with no text
def create_button_grid(index):
    #Disable buttons after testing
    MaxCols = MaxRows = 12
    return [[sg.Button('', size=(2, 1), pad = (0, 0), key = (index, row, col)) 
             for col in range(MaxCols)] for row in range(MaxRows)]
"""

def create_button_grid(index):
    def get_value():
        for lst in Map:
            for v in lst:
                yield v
    gen = get_value()
    MaxCols = MaxRows = 12
    return [[sg.Button(next(gen), size=(2, 1), pad = (0, 0), key = (index, row, col)) 
             for col in range(MaxCols)] for row in range(MaxRows)]   

layout = [create_button_grid(0)]

window = sg.Window('Button Grid', layout, finalize = True)

while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        break
        
    print(event)

window.close()