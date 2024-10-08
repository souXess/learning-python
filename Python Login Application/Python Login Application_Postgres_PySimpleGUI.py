#Description: Demonstrating the concept of creating and authenticating login credentials using a database (Postgres) and GUI (PySimpleGUI).
#Author: souXess
#Created: 01Sep2024
#Last Modified: 03Sep2024 

import re
import datetime as dt
import hashlib as hl
import psycopg2 as pg
import PySimpleGUI as sg

#Create a connection to the simple_login_database
conn = pg.connect(database = 'simple_login_example',
                       user = 'postgres',
                       host = 'localhost',
                       password = '<insert password>',
                       port = 5432)

#Define login window layout
layout_window1 = [[sg.Text('Please enter your username and password to login.')],
          [sg.Text('Username:'), sg.Input(key = '-USERNAME-')],
          [sg.Text('Password:'), sg.Input(password_char = '*', key = '-PASSWORD-')],
          [sg.Push(), sg.Button('Exit', key = '-EXIT-'), sg.Button('Login', key = '-LOGIN-'), sg.Push()],
          [sg.Text('New user?'), sg.Text('Create Account', enable_events = True, key = '-CREATE_ACCOUNT-', colors = '#90EE90')]]

window1 = sg.Window('Python Login Application', layout_window1, finalize = True)

window1['-EXIT-'].set_cursor('hand2')
window1['-LOGIN-'].set_cursor('hand2')
window1['-CREATE_ACCOUNT-'].set_cursor('hand2')
window1['-CREATE_ACCOUNT-'].Widget.bind('<Enter>', lambda _: window1['-CREATE_ACCOUNT-'].update(font=(None, 10, 'underline')))
window1['-CREATE_ACCOUNT-'].Widget.bind('<Leave>', lambda _: window1['-CREATE_ACCOUNT-'].update(font=(None, 10)))

while True:
    event, values = window1.read()
    
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
        
    if event == '-LOGIN-':
        if values['-USERNAME-'] == '' and values['-PASSWORD-'] == '':
            sg.popup('Please enter your username and password.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
        elif values['-USERNAME-'] == '':
            sg.popup('Please enter your username.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
        elif values['-PASSWORD-'] == '':
            sg.popup('Please enter your password.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
        else:
            #Check simple_login_example db to see if username exists and retrieve matching username and corresponding
            #hash_value and pwd_date values
            cur = conn.cursor()
            cur.execute("SELECT username, hash_value, pwd_date FROM users WHERE lower(username) = %s", (values['-USERNAME-'].lower(),))
            res = cur.fetchone()
            cur.close()
            
            if res is None:
                sg.popup("The username '" + values['-USERNAME-'] + "'" + " does not exist. Please re-enter your username.",
                         text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
            else:   
                StoredUsername = res[0]
                StoredHashValue = res[1]
                StoredPwdDate = res[2]
                
                #Create hash value of the cancatenation of the entered username and password and the stored password
                #date associated with the username
                sha256 = hl.sha256()
                sha256.update(StoredUsername.lower().encode() + values['-PASSWORD-'].encode() + StoredPwdDate.encode())
                LoginHashValue = sha256.hexdigest()
                
                if LoginHashValue != StoredHashValue:
                    sg.popup('The password entered is incorrect. Please re-enter your password.', 
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                else:
                    sg.popup('Welcome ' + StoredUsername + '! You have successfully logged in.', title = 'Welcome')
                                        
                    break
                    
    if event == '-CREATE_ACCOUNT-':
        tooltip_password = ("Please create a password.\n\n" + 
          'Password requirements:\n' +
          '-Between 8 and 15 characters\n' +
          '-Contains at least 1 uppercase letter\n' +
          '-Contains at least 1 lowercase letter\n' +
          '-Contains at least 1 special character (!, @, #, $, %, ^, &, *, (, ))\n' +
          '-Contains at least 1 number')

        #Define create account window layout
        layout_window2 = [[sg.Text('Please enter a username and password.')],
            [sg.Text('Username:'), sg.Input(key = '-USERNAME-', tooltip = 'Please create a username between 3 and 15 characters in length')],
            [sg.Text('Password:'), sg.Input(password_char = '*', key = '-PASSWORD-', tooltip = tooltip_password)],
            [sg.Text('Confirm \nPassword:'), sg.Input(password_char = '*', key = '-CONFIRM_PASSWORD-')],               
            [sg.Push(), sg.Button('Cancel', key = '-CANCEL-'), sg.Button('Create Account', key = '-CREATE_ACCOUNT-'), sg.Push()]]
        
        window2 = sg.Window('Create Account', layout_window2, finalize = True, modal = True)
        
        window2['-CANCEL-'].set_cursor('hand2')
        window2['-CREATE_ACCOUNT-'].set_cursor('hand2')
        
        while True:
            event, values = window2.read()
    
            if event == sg.WIN_CLOSED or event == '-CANCEL-':
                break
                
            if event == '-CREATE_ACCOUNT-':
                #Check user's password for invalid special characters and remove duplicates
                InvalidSpecialChar = list(dict.fromkeys(re.findall("[^a-zA-Z0-9!@#$%^&*()]", values['-PASSWORD-'])))
    
                #Check user's password for special characters
                SpecialChar = re.findall("[!@#$%^&*()]", values['-PASSWORD-'])
        
                #Check user's password for uppercase letters
                UpperCaseLetter = re.findall("[A-Z]", values['-PASSWORD-'])
    
                #Check user's password for lowercase letters
                LowerCaseLetter = re.findall("[a-z]", values['-PASSWORD-'])
    
                #Check user's password for numbers
                Number = re.findall("[0-9]", values['-PASSWORD-'])
            
                #Check simple_login_example db to see if username already exists
                cur = conn.cursor()
                cur.execute("SELECT username FROM users WHERE lower(username) = %s", (values['-USERNAME-'].lower(),))
                res = cur.fetchone()
                cur.close()
            
                if values['-USERNAME-'] == '' and values['-PASSWORD-'] == '':
                    sg.popup('Please enter a username and password.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif values['-USERNAME-'] == '':
                    sg.popup('Please enter a username.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif values['-PASSWORD-'] == '':
                    sg.popup('Please enter a password.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(values['-USERNAME-']) < 3:
                    sg.popup('The username you entered has less than 3 characters.\nPlease enter a username between 3 and 15 characters in length.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(values['-USERNAME-']) > 15:
                    sg.popup('The username you entered has more than 15 characters.\nPlease enter a username between 3 and 15 characters in length.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(values['-PASSWORD-']) < 8:
                    sg.popup('The password you entered has less than 8 characters.\nPlease enter a password between 8 and 15 characters in length.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(values['-PASSWORD-']) > 15:
                    sg.popup('The password you entered has more than 15 characters.\nPlease enter a password between 8 and 15 characters in length.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(InvalidSpecialChar) > 0:
                    sg.popup('The password you entered contains one or more of the invalid special character(s): \'' + 
                             '\', \''.join('!#%') + '\'' +
                             '\nPlease re-enter your password using only the allowed special characters: !, @, #, $, %, ^, &, *, (, )',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(SpecialChar) < 1:
                    sg.popup('The password you entered does not contain any special characters.\n' +
                             'Please re-enter your password being sure it contains at least 1 of the allowed special characters: !, @, #, $, %, ^, &, *, (, )',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(UpperCaseLetter) < 1:
                    sg.popup('The password you entered does not contain any uppercase letters.\n' +
                             'Please re-enter your password being sure it contains at least 1 uppercase letter.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(LowerCaseLetter) < 1:
                    sg.popup('The password you entered does not contain any lowercase letters.\n' +
                             'Please re-enter your password being sure it contains at least 1 lowercase letter.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif len(Number) < 1:
                    sg.popup('The password you entered does not contain any numbers.\n' +
                             'Please re-enter your password being sure it contains at least 1 number.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif values['-CONFIRM_PASSWORD-'] == '':
                    sg.popup('Please confirm your password.', text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif res is not None:
                    sg.popup('The username \'' + values['-USERNAME-'] + '\'' + ' already exists. Please create a different username.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                elif values['-PASSWORD-'] != values['-CONFIRM_PASSWORD-']:
                    sg.popup('The passwords do not match.\nPlease re-enter your password and confirm.',
                             text_color = '#FF0000', background_color = '#D3D3D3', title = 'Error')
                else:
                    PwdDateTime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
                    #Create unique hash value by concatenating and then hashing Username, Password and PwdDateTime
                    sha256 = hl.sha256()
                    sha256.update(values['-USERNAME-'].lower().encode() + values['-PASSWORD-'].encode() + PwdDateTime.encode())
                    StoredHashValue = sha256.hexdigest()
    
                    #Insert Username, StoredHashValue and PwdDateTime into the simple_login_example db
                    cur = conn.cursor()
                    cur.execute("INSERT INTO users(username, hash_value, pwd_date) VALUES(%s, %s, %s)", (values['-USERNAME-'], StoredHashValue, PwdDateTime))
                    conn.commit()
                    cur.close()
    
                    sg.popup('New user account successfully created. Please login.', title = 'Success')
        
                    break
            
        window2.close()

conn.close()
window1.close()
