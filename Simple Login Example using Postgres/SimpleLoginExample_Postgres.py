#Description: Practicing the concept of creating and authenticating login credentials using a database
#Author: souXess
#Created: 04Mar2024
#Last Modified: 05Mar2024

import re
import datetime as dt
import psycopg2 as ppg2

#Create a connection to the simple_login_database
conn = ppg2.connect(database = 'simple_login_example',
                       user = 'postgres',
                       host = 'localhost',
                       password = '<insert pwd>',
                       port = 5432)

def authenticate_user():
    print("Please enter your username.\n")
    
    LoginUsername = input("Username: ")
    
    print()
    
    #Check simple_login_example db to see if username exists and retrieve matching username and corresponding
    #hash_value and pwd_date values
    cur = conn.cursor()
    cur.execute("SELECT username, hash_value, pwd_date FROM users WHERE lower(username) = %s", (LoginUsername.lower(),))
    res = cur.fetchone()
        
    while res is None:
        print("The username '" + LoginUsername + "'" + " does not exist. Please re-enter your username.\n")
        LoginUsername = input("Username: ")
        cur.execute("SELECT username, hash_value, pwd_date FROM users WHERE lower(username) = %s", (LoginUsername.lower(),))
        res = cur.fetchone()
        print()
        
    StoredUsername = res[0]
    StoredHashValue = res[1]
    StoredPwdDate = res[2]
        
    cur.close()
    conn.close()
            
    print()
    
    print("Please enter your password.\n")
    
    LoginPassword = input("Password: ")
    
    print()
    
    LoginHashValue = hash(StoredUsername.lower() + LoginPassword + StoredPwdDate)
    
    while LoginHashValue != StoredHashValue:
        print("The password you entered is incorrect.\n"
             "Please re-enter your password.\n")
        LoginPassword = input("Password: ")
        LoginHashValue = hash(StoredUsername.lower() + LoginPassword + StoredPwdDate)
        print()
        
    print("Welcome, " + StoredUsername + "! You have successfully logged in.")
    
    exit()

def create_password(Username):
    Password = input("Password: ")
    
    print()
    
    #Check user's password for invalid special characters and remove duplicates
    InvalidSpecialChar = list(dict.fromkeys(re.findall("[^a-zA-Z0-9!@#$%^&*()]", Password)))
    
    #Check user's password for special characters
    SpecialChar = re.findall("[!@#$%^&*()]", Password)
        
    #Check user's password for uppercase letters
    UpperCaseLetter = re.findall("[A-Z]", Password)
    
    #Check user's password for lowercase letters
    LowerCaseLetter = re.findall("[a-z]", Password)
    
    #Check user's password for numbers
    Number = re.findall("[0-9]", Password)
    
    if len(Password) < 8:
        print("The password you entered has less than 8 characters.\n" +
              "Please enter a password between 8 and 15 characters in length.\n")
        create_password(Username)
    elif len(Password) > 15:
        print("The password you entered has more than 15 characters.\n" +
              "Please enter a password between 8 and 15 characters in length.\n")
        create_password(Username)
    elif len(InvalidSpecialChar) > 0:
        print("The password you entered contains one or more of the invalid special character(s): '" + 
              "', '".join(InvalidSpecialChar) + "'" +
              "\nPlease re-enter your password using only the allowed special characters: !, @, #, $, %, ^, &, *, (, )\n")
        create_password(Username)
    elif len(SpecialChar) < 1:
        print("The password you entered doesn't contain any special characters.\n" +
             "Please re-enter your password being sure it contains at least 1 of the allowed special characters: !, @, #, $, %, ^, &, *, (, )\n")
        create_password(Username)
    elif len(UpperCaseLetter) < 1:
        print("The password you entered doesn't contain any uppercase letters.\n" +
             "Please re-enter your password being sure it contains at least 1 uppercase letter.\n")
        create_password(Username)
    elif len(LowerCaseLetter) < 1:
        print("The password you entered doesn't contain any lowercase letters.\n" +
             "Please re-enter your password being sure it contains at least 1 lowercase letter.\n")
        create_password(Username)
    elif len(Number) < 1:
        print("The password you entered doesn't contain any numbers.\n" +
             "Please re-enter your password being sure it contains at least 1 number.\n")
        create_password(Username)
    else: print("Please re-enter your password.\n")

    VerifyPassword = input("Password: ")
    
    print()

    while Password != VerifyPassword:
        print("The passwords don't match.\n" +
             "Please re-enter your password.\n")
        VerifyPassword = input("Password: ")
        print()
        
    PwdDateTime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    #Create unique hash value by concatenating and then hashing Username, Password and PwdDateTime
    StoredHashValue = hash(Username.lower() + Password + PwdDateTime)
    
    #Insert Username, StoredHashValue and PwdDateTime into the simple_login_example db
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username, hash_value, pwd_date) VALUES(%s, %s, %s)", (Username, StoredHashValue, PwdDateTime))
    conn.commit()
    cur.close()
    
    print("Username and password successfully created. Please login.\n")

    authenticate_user()

def create_username():
    print("Please create a username between 3 and 15 characters in length.\n")

    Username = input("Username: ")
    
    print()
    
    #Check simple_login_example db to see if username already exists
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE lower(username) = %s", (Username.lower(),))
    res = cur.fetchone()
        
    while len(Username) < 3 or len(Username) > 15 or res is not None:
        if len(Username) < 3:
            print("The username you entered has less than 3 characters.\n" +
                  "Please enter a username between 3 and 15 characters in length.\n")
            Username = input("Username: ")
            print()
        elif len(Username) > 15:
            print("The username you entered has more than 15 characters.\n" +
                  "Please enter a username between 3 and 15 characters in length.\n")
            Username = input("Username: ")
            print()
        elif res is not None:
            print("The username '" + Username + "'" + " already exists. Please create a different username.\n")
            Username = input("Username: ")
            cur.execute("SELECT username FROM users WHERE lower(username) = %s", (Username.lower(),))
            res = cur.fetchone()
            print()    
            
    cur.close()

    print("Please create a password.\n\n" + 
          "Password requirements:\n" +
          "-Between 8 and 15 characters\n" +
          "-Contain at least 1 uppercase letter\n" +
          "-Contain at least 1 lowercase letter\n" +
          "-Contain at least 1 special character (!, @, #, $, %, ^, &, *, (, ))\n" +
          "-Contain at least 1 number\n")

    create_password(Username)
     
create_username()
