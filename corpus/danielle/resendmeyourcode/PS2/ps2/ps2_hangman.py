# 6.00 Problem Set 2
# Name: Danielle Chow
#Collaborators (Discussion): Sammy Khalifa
#Collaborators (Identical Solution):
#Time: 2:00
# Hangman
#


# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# load the list of words into the wordlist variable
# so that it can be accessed from anywhere in the program


def template_generator(length):  #Function to create the sequence of blanks and spaces that reflects the unknown word
    i=0
    template=''
    while i<length:     #Doesn't make the template longer than it needs to be
        template=template + '_ '    #Template will have one extra space that doesn't really matter
        i=i+1
    return template
    


def template_changer(template, index, guess):  #Function that changes the sequence of blanks and spaces as letters in the word are guessed
        n=len(template)
        j=0
        Template='' #Blank dummy variable
        while j<n:  #Goes through template blank by blank
            if j/2==index:  #if j/2 is equal to the idex of the location of the guess in the word then adds the guess letter and a space
                Template+=guess+' '
            else:
                Template+=template[j]+' '   #else repeats whatever was previously in the template and a space
            j=j+2       #iterates by two to account for spaces
        template=Template   #reassigns dummy variable to actual template
        return template


wordlist = load_words() #Loads words
word=choose_word(wordlist) #Chooses a random word

guesses=8   #Sets maximum number of incorrect guesses

template=template_generator(len(word))  #Uses the template generator function to create the series of spaces and underscores known as the "template"

print('Welcome to the game, Hangman!') 
print('I am thinking of a word that is '+ str(len(word)) + ' letters long.')
##print(word)

letters=string.lowercase    #creates the string of available letters

while(str.find(template,'_'))>-1:   #Only prompts player for guess if there are blanks
    print('-----------------')
    print('You have ' + str(guesses) + ' guesses left.')
    print('Available letters: ' + str(letters))
    guess=raw_input('Please guess a letter: ')

    
    if len(guess)>1:    #Checks to make sure user is only guessing one letter a a time
        print('Only guess one letter at a time!')
##    elif guess is not char:           #Isn't necessary, but couldn't figure out how to handle a numeric input!
##        print('Only letters please!')  
    elif str.find(letters,guess)==-1:   #Prompts user to not guess the same letter, wrong or right, more than once
        print('You have already guessed this letter.Try again.')
        print(template)

    else:
        letters=str.replace(letters,guess,'') #Removes guess from the list of available letters
        print(letters)

        start=0     #Initial starting index of the search feature
        index=str.find(word,str(guess),start,len(word)) #searches the word for the guessed letter between the starting index and the end of the word and outputs the index of the guess
        template=template_changer(template, index, guess) #Updates the template with the fist instance of the guess 
        if index==-1:   #if guess is incorrect, user loses a guess and is told the guess was incorrec
            guesses=guesses-1
            print('Oops! That letter is not in my word:' + str(template))
        else:
            while index>(-1):   #Checks for more than one instance of a letter
                index=str.find(word,str(guess),index+1,len(word))   #Searches for the guess between the last found instance and the end of the word
                template=template_changer(template, index, guess)   #Updates template
            print('Good guess: ' + str(template))
        if guesses<0:   #checks if the user has run out of guess and updates the template to remove underscores and ends loop
            template=word
if guesses<0:   #if the user cannot guess the word in the alloted number of guesses, they are told they have lost and told the word
    print('Sorry! You lost. The word was '+ str(word))
else:   #if the user can guess the word in the alloted number of guesses, they are congratualted on being uber cool :D
    print('Congratualtions, you won!')


