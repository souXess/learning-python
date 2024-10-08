#Description: Practicing the concept of creating and authenticating login credentials
#Author: souXess
#Created: 15Feb2024
#Last Modified: 15Feb2024

import re
import datetime

def authenticate_user(Username,PwdDateTime,StoredHashValue):
    print("Please enter your username.\n")
    
    LoginUsername = input("Username: ")
    
    print()
    
    print("Please enter your password.\n")
    
    LoginPassword = input("Password: ")
    
    print()
    
    LoginHashValue = hash(LoginUsername.lower() + LoginPassword + PwdDateTime.strftime("%Y-%m-%d %H:%M:%S.%f"))
    
    while LoginHashValue != StoredHashValue:
        print("The username and/or password you entered is incorrect.\n"
             "Please re-enter your username.\n")
        LoginUsername = input("Username: ")
        print()
        print("Please re-enter your password.\n")
        LoginPassword = input("Password: ")
        print()
        LoginHashValue = hash(LoginUsername.lower() + LoginPassword + PwdDateTime.strftime("%Y-%m-%d %H:%M:%S.%f"))
        
    print("Welcome, " + LoginUsername + "! You have successfully logged in.")
    
    exit()

def create_password(Username):
    Password = input()
    
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
              "Please enter a password between 8 and 15 characters in lengt.\n")
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

    VerifyPassword = input()
    
    print()

    while Password != VerifyPassword:
        print("The passwords don't match.\n" +
             "Please re-enter your password.\n")
        VerifyPassword = input()
        print()
        
    PwdDateTime = datetime.datetime.now()
    
    #Create unique hash value by concatenating and then hashing Username, Password and PwdDateTime
    StoredHashValue = hash(Username.lower() + Password + PwdDateTime.strftime("%Y-%m-%d %H:%M:%S.%f"))

    print("Username and password successfully created. Please login.\n")

    authenticate_user(Username,PwdDateTime,StoredHashValue)

def create_username():
    print("Please create a username between 3 and 15 characters in length.\n")

    Username = input()
    
    print()

    while len(Username) < 3 or len(Username) > 15:
        if len(Username) < 3:
            print("The username you entered has less than 3 characters.\n" +
                  "Please enter a username between 3 and 15 characters in length.\n")
            Username = input()
            print()
        elif len(Username) > 15:
            print("The username you entered has more than 15 characters.\n" +
                  "Please enter a username between 3 and 15 characters in length.\n")
            Username = input()
            print()

    print("Please create a password.\n" + 
          "Password requirements:\n" +
          "-Between 8 and 15 characters\n" +
          "-Contain at least 1 uppercase letter\n" +
          "-Contain at least 1 lowercase letter\n" +
          "-Contain at least 1 special character (!, @, #, $, %, ^, &, *, (, ))\n" +
          "-Contain at least 1 number\n")

    create_password(Username)
     
create_username()
