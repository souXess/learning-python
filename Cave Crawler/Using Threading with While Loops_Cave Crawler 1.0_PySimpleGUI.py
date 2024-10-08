#Description: Breaking out of while loops using threading to ensure the window can read the event.
#Author: souXess
#Created: 08Oct2024
#Last Modified: 08Oct2024

import threading as t
import time
import PySimpleGUI as sg

layout = [[sg.Text('', key = '-TEXT-')], 
          [sg.Button('Start', key = '-START-'), sg.Button('Pause', key = '-PAUSE-')]]

window = sg.Window('Threading Test', layout, finalize = True)

while True:
    event, values = window.read()
    
    print(event)
        
    def some_function():
        i = 0
        j = 0
        while i < 11:
            if event == '-PAUSE-':
                break
            while j < 11:
                if event == '-PAUSE-':
                    break
                window['-TEXT-'].update(f'i = {i}, j = {j}')
                i += 1
                j += 1
                window.refresh()
                time.sleep(3)
        
        window['-TEXT-'].update('While loops have stopped.')
        window.refresh()
    
    if event == sg.WIN_CLOSED:
        break
    elif event == '-START-':
        t1 = t.Thread(target = some_function)
        t1.start()

window.close()