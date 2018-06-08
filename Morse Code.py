#######################
#                     #
#   Morse Code Quiz   #
#    Emer Campbell    #
#      June 2018      #
#                     #
#######################


#import libraries#
from random import randint
import re
import datetime

##set up dictionary to hold morse code equivilents##

CODE = { ' ': '_', 'A' : '.-', 'B' : '-...', 'C' : '-.-.', 'D' : '-..' ,'E' : '.', 'F' : '..-.',
        'G' : '--.' ,'H' : '....' , 'I' : '..' ,'J' : '.---' , 'K' : '-.-' , 'L' : '.-..',
        'M' : '--' , 'N' : '-.' , 'O' : '---' , 'P' : '.--.' , 'Q' : '--.-' , 'R' : '.-.' , 'S' : '...', 
        'T' : '-' , 'U' : '..-' , 'V' : '...-' , 'W' : '.--' , 'X' : '-..-' , 'Y' : '-.--' , 'Z' : '--..',
         '2' : '..---' , '3' : '...--' , '4' : '....-' , '5' : '.....', '6' : '-...' , '7' : '--...', '8' : '---..'}

###define functions###

#check user login and password against values in text file
def login():
    username = ' '
    password = ' '
    while username != 'exit':
        username = input("Please enter your username or exit to exit: ")
        if username == 'exit':
            print('Goodbye')
            break
        password = input("Please enter your password: ")
        try:
            for line in open("logins.txt","r").readlines():
                login_info = line.split()
                if username == login_info[0] and password == login_info[1]:
                    print("Correct credentials! ")
                    return True, username
            print("Incorrect credentials. ")
        except:
            print('We cannot load the file.  You can continue with the game but will not be able to save your score or view the leaderboard ')
            return True, 'null'
    

#generate a sentence by randomly choosing and concatenating items in 4 lists
def genSentence():
    properNoun = ['EMER', 'JOHN','MARY','SARA','RUBY','JAKE','CARL']
    verb = ['KICKS','STEALS','TAKES','FINDS','LOSES','HIDES','DROPS']
    determiner = ['2','3','4','5','6','7','8']
    noun = ['PUMPKINS','PICTURES','MONSTERS','BICYCLES','NOTHINGS','KINGDOMS','DIAMONDS']
    sentence = properNoun[randint(0,6)] + " " + verb[randint(0,6)] + " " + determiner[randint(0,6)] + " " + noun[randint(0,6)]
    return sentence


#loop through each item in the sentence and convert to morse code symbol using dictionary
def morseConvert(sentence):
    code = ''
    for i in sentence:
        mSymbol = CODE[i]
        code += ('/' + mSymbol)
    return code

#obtain user guess and validate it by calling isValid method
def getInput():
    correctChars = False
    correctLength = False
    while correctChars == False or correctLength == False:
        userSentence = input('Answer:  ')
        correctChars, correctLength = isValid(userSentence)
        if correctChars == False:
            print('Remember to only use letters, numbers and spaces ')
        if correctLength == False:
            print('Remember each sentence contains exactly 4 words ')
    return userSentence

# validate sentence by checking the number of words and that it only contains [A-Z],[0-9] or space
def isValid(sentence):
    correctChars = True
    correctLength = True
    if not(all(x.isalpha() or x.isspace() or x.isnumeric() for x in sentence)):
        correctChars = False
    if not(sentence.count(' ')==3):
        correctLength = False
    return correctChars, correctLength

#colculate score: - point if incorrect number of characters in each word, - point for each incorrect letter in each word
def getScore(programSentence, userSentence):
    score = 22
    userWords = userSentence.split()
    programWords = programSentence.split()

    #checks user has identified correct number of characters in each word
    if len(userWords[0]) !=4:
        score -=1
    if len(userWords[1]) !=5:
        score -=1
    if len(userWords[2]) !=1:
        score -=1
    if len(userWords[3]) !=8:
        score -=1

    #need to find which word is shorter(user's or computer's) to avoid index out of range exception when looping through to compare characters
    for i in range (0,4):
        uW = userWords[i]
        pW = programWords[i]
        if len(uW) < len(pW):
            length = len(uW)
        else:
            length = len(pW)
        for j in range (length):
            if uW[j] != pW[j]:
                score -=1
    return score

#output feedback based on score and give option to save/view leaderboard.  Call saveView function
def feedback(username, score):
    feedback = ' '
    if score > 20:
        feedback = 'Congratulations, there\' s a job for you at Bletchley Park'
    elif score > 18:
        feedback = 'Not bad, but you\'re not quite ready to crack the enigma code just yet'
    elif score > 10:
        feedback = 'I don\'t think you\'re ready to work at Bletchley park but we\'ll be happy to let you visit'
    else:
        feedback = 'Are you sure you\'re not confusing morse code with something else entirely?'
        
    print('Your guessed:   ', userSentence, '\n')
    print('The Morse Code was:    ', morseSentence, '\n')
    print('The original sentence was:   ', programSentence, '\n')
    print('You scored:  ', score, ' ', feedback, '\n')
    
    
    if username != 'null' : # if user could not login they should not be able to save the score
        save = input('would you like to save your score and view the leaderboard? Y/N:   \n')
        if save == 'Y' or 'y' or 'YES' or 'yes' or 'Yes':
            saveView(username, score)

# save details to a text file.  Build leaderboard of previous scores
def saveView(username, score):
    currentDT = str(datetime.datetime.now())
    output = username + ' ' + str(score) + ' ' + currentDT

    try:
        writeFile = open('HighScores.txt', 'a')
        writeFile.write(output + '\n')
        writeFile.close()

        with open("HighScores.txt") as textFile:
            scoresInput = [line.split() for line in textFile]
        sortedScores = sorted(scoresInput, key = lambda x: int(x[1]), reverse = True)
        print('----------------Leaderboard-----------------')
        print("%-15s%15s%15s"%("Username","Score","Date"))

        if len(sortedScores) < 6: #check if less than 5 names in text file to avoid index out of range exception
            times = len(sortedScores)
        else:
            times = 5
              
        for i in range (times):
            print("%-15s%15s%15s"%(sortedScores[i][0],sortedScores[i][1],sortedScores[i][2]))

        
    except:
        print('There seems to be a problem with the file.  Please try again later ')


####main program####
        
playAgain = 'Y' 
validUser, username = login() #validate user login

while playAgain.upper() == 'Y' or 'y' or 'YES' or 'yes' or 'Yes': #allow user to play again after each guess
    print('\n Welcome to the Morse Code Quiz ')
    
    programSentence=(genSentence()) #generate a unique sentence

    morseSentence = morseConvert(programSentence) #convert sentence to morse code
    print('\n Convert the following sentence to English.  Remeber the sentence contains 5 words.  You can only use '
          'letters, number and spaces.  Each letter is seperated by a \ and a space represented by the _ symbol ') #output converted sentence
    print(morseSentence)

    #print(programSentence) for purpose of testing during development
    

    userSentence = getInput()#collect user input
            
    userSentence = userSentence.upper()#convert to all upper case(dictionary stores upper case characters only
    score = getScore(programSentence, userSentence) #collect score

    feedback(username, score)

    playAgain = input("\n would you like to play again? Y/N: ")

    
        
    
    


    

    
    



        
    


