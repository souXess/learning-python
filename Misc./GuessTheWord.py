#Description: A simple game where a player tries to guess the word the PC has selected.
#This is the first script I created to teach myself pyhton.
#Author: souXess
#Created: 11Feb2024
#Last modified: 15Feb2024

import re
import random
import time

def introduce_game():
    GameTitle = ["Guess", "The", "Word", "\nCreated", "by:"]
    
    GameCreator = ["s", "o", "u", "X", "e", "s", "s\n"]
    
    for x in GameTitle:
        print(x, end = ' ')
        time.sleep(.25)
    
    time.sleep(.75)
            
    for x in GameCreator:
        print(x, end = '')
        time.sleep(.5)

    time.sleep(1.5)
        
def get_player_guess(SelectedWord, WordList):
    print()
    
    PlayerGuess = input()
    
    #Check if player's input matches any of the words in WordList
    WordExists = PlayerGuess in WordList
       
    #If player didn't enter a word
    if PlayerGuess == "":
        print("\nYou didn't enter a word. Please enter your guess and press 'Enter'.")
        get_player_guess(SelectedWord, WordList)
    #If player's input doesn't match any of the words in WordList    
    elif WordExists == False:
        print("\nThe word you entered doesn't match any in the list." +
              "\nPlease select one of the 5 words from the list (" + ", ".join(WordList) + ") and press 'Enter'.")
        get_player_guess(SelectedWord, WordList)
    #Player's input matches SelectedWord
    elif PlayerGuess == SelectedWord:
        print("\nYou've guessed: " + PlayerGuess +
             "\nAnd the word I selected was...")
        time.sleep(3)
        print("\n...")
        time.sleep(3)
        print("\nalso " + SelectedWord + ". Congratulations! You've guessed correctly." +
             "\nWould you like to play again? Type 'Y' for yes or 'N' for no and then press 'Enter'.")
        print()
        PlayAgain = input()
        while PlayAgain.upper().strip() != "Y" and PlayAgain.upper().strip() != "N":
            print("\nPlease only type 'Y' or 'N' and press 'Enter'.")
            print()
            PlayAgain = input()
        if PlayAgain.upper().strip() == "Y":
            print("\nGreat!" + "\nLet me go ahead and select another word...")
            time.sleep(3)
            print("\numm...")
            time.sleep(3)
            SelectedWord = WordList[random.randrange(0, 5)]  
            print("\nOkay. I've selected a word. Can you guess it?")
            get_player_guess(SelectedWord, WordList)
        else: 
            print("\nAlright. Hope to play again with you soon. Good bye!")
            exit()
    #Player's input doesn't match SelectedWord     
    else:
        print("\nYou've guessed: " + PlayerGuess +
             "\nAnd the word I selected was...")
        time.sleep(3)
        print("\n...")
        time.sleep(3)
        print("\n" + SelectedWord + ". Unfortunately, you didn't guess correctly." +
             "\nWould you like to play again? Type 'Y' for yes or 'N' for no and then press 'Enter'.")
        print()
        PlayAgain = input()
        while PlayAgain.upper().strip() != "Y" and PlayAgain.upper().strip() != "N":
            print("\nPlease only type 'Y' or 'N' and press 'Enter'.")
            print()
            PlayAgain = input()
        if PlayAgain.upper().strip() == "Y":
            print("\nGreat!" + "\nLet me go ahead and select another word...")
            time.sleep(3)
            print("\numm...")
            time.sleep(3)
            SelectedWord = WordList[random.randrange(0, 5)]  
            print("\nOkay. I've selected a word. Can you guess it?")
            get_player_guess(SelectedWord, WordList)
        else: 
            print("\nAlright. Hope to play again with you soon. Good bye!")
            exit()
    
def get_player_words():
    print()
    
    PlayerWords = input()
    
    #Split player's input via white space
    WordList = PlayerWords.split(" ")
    
    #Create duplicate word list
    DuplicateWords = []
    for x in WordList:
        a = WordList.count(x)
        if a > 1:
            if DuplicateWords.count(x) == 0:
                DuplicateWords.append(x)
                
    #Check player's input for any special characters and/or numbers and remove duplicates
    SpecialCharNum = list(dict.fromkeys(re.findall("[^a-zA-Z ]", PlayerWords)))
    
    #If player didn't enter any words
    if PlayerWords == "":
        print("\nYou didn't enter any words." + 
              "\nPlease enter exactly 5 unique words separating each with a space and press 'Enter'.")
        get_player_words()
    #If player's input is not exactly 5 words AND contains special characters and/or numbers
    elif len(WordList) != 5 and len(SpecialCharNum) > 0:
        print("\nYou entered: " + ", ".join(WordList) +
              "\nYou didn't enter the correct number of words and you also used the special character(s)/number(s): " 
              + ", ".join(SpecialCharNum) +
              "\nPlease enter exactly 5 unique words separating each with a space and press 'Enter'." +
              "\n*Be sure not to use any special characters or numbers.")
        get_player_words()
    #If player's input is not exactly 5 words AND doesn't contain any special characters and/or numbers
    elif len(WordList) != 5 and len(SpecialCharNum) == 0:
        print("\nYou entered: " + ", ".join(WordList) +
              "\nYou didn't enter the correct number of words." +
              "\nPlease enter exactly 5 unique words separating each with a space and press 'Enter'.")
        get_player_words()
    #If player's input is exactly 5 words AND contains special characters and/or numbers
    elif len(WordList) == 5 and len(SpecialCharNum) > 0:
        print("\nYou entered: " + ", ".join(WordList) +
              "\nYou entered the correct number of words but you used the special character(s)/number(s): " 
              + ", ".join(SpecialCharNum) +
              "\nPlease enter exactly 5 unique words separating each with a space and press 'Enter'." +
              "\n*Be sure not to use any special characters or numbers.")
        get_player_words()
    #If player's input contains duplicate words    
    elif len(DuplicateWords) > 0:
        print("\nYou entered: " + ", ".join(WordList) +
              "\nYou entered the following word(s) more than once: " + ", ".join(DuplicateWords) +
              "\nPlease enter exactly 5 unique words separating each with a space and press 'Enter'.")    
        get_player_words()
    #If player's input is exactly 5 unique words AND doesn't contain any special characters and/or numbers
    else :
        print("\nYou have chosen the words: " + ", ".join(WordList) +
              "\nNow I will randomly select one of the words from your list. Let's see, umm...")
        time.sleep(3)
        print("\numm...")
        time.sleep(3)
        #Randomly select a word from WordList
        SelectedWord = WordList[random.randrange(0, 5)]    
        print("\nOkay. I've selected a word. Can you guess which one it is?" +
             "\nPlease enter your guess and press 'Enter'.")        
        get_player_guess(SelectedWord, WordList)

def get_player_input():
    print("\nHello there!" +
          "\nWould you like to play Guess The Word with me? Type 'Y' for yes or 'N' for no and then press 'Enter'.")
    
    print()
    
    PlayerInput = input()
            
    while PlayerInput.upper().strip() != "Y" and PlayerInput.upper().strip() != "N":
        print("\nPlease only type 'Y' or 'N' and press 'Enter'.")
        print()
        PlayerInput = input()
        
    if PlayerInput.upper().strip() == 'Y':
        print("\nGreat!" + 
              "\nPlease enter exactly 5 unique words separating each with a space being sure not to use any" +
              "\nspecial characters or numbers and press 'Enter'.")
        get_player_words()
    else:
        print("\nOh well, maybe next time. Good bye!")
        exit()
        
introduce_game()

get_player_input()