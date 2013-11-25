# Problem Set 3A
# Name: Danielle Chow
# Collaborators (Discussion): Sammy Khalia
# Collaborators (Identical Solution): 
# Time: 3:00
#Late Days:1

# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first go.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    #
    WordScore=0 #the initial "dummy" value of WordScore that is replaced as soon as the program runs
    i=0 #allows every letter to be scored independently as i iterates up
    length=len(word) #calculates the length of the word
    while i<length: #make sure function stops after every letter in the word has been scored
        WordScore=WordScore + SCRABBLE_LETTER_VALUES[word[i]] #adds every letters individual score to the total wordscore
        i=i+1 #iterates our counter up

    WordScore=WordScore*length #multiplies the score of the word by the length of the word
    
    if length==n: #condition that allows the score to be increased by 50 if all letters in the hand are used
            WordScore=WordScore + 50
    
    return WordScore

##    
    
#
# Problem #2: Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #
    i=0 #inital value of the counter
    n=len(word) 
    Hand_Copy=hand.copy() #makes a copy of the hand
    while i<n:
        Hand_Copy[word[i]]=Hand_Copy[word[i]]-1 #Removes a letter in the word from the hand via editing the index
        i=i+1
    return Hand_Copy

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    #
    copy=hand.copy()
    Answer=True
    i=0
    n=len(word)
    while i<n:
        if Answer==True:
            if word[i] in hand:
                if copy[word[i]]<=0:
                    Answer=False
                else:
                    copy[word[i]]=copy[word[i]]-1
                    if word in word_list:
                        Answer=True
                    else:
                        Answer=False
            else:
                Answer=False
        i=i+1
    return Answer
    
#
# Problem #4: Playing a hand
#

def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    #
    length=0
    for letter in hand.keys():
        ##for j in range(hand[letter]):
            length=length+(hand[letter]) 
##    i=0
##    length=0
##    while i<len(hand):
##        length=length + hand[i]
##        i=i+1
    return length


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    # BEGIN PSEUDOCODE <-- Remove this comment when you code this function
    # Keep track of two numbers: the number of letters left in your hand and the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is a single period:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not a single period):
        
            # If the word is not valid:
            
                # Reject invalid word (print a message)

            # Otherwise (the word is valid):

                # Tell the user how many points the word earned, and the updated total score 
                
                # Update hand and show the updated hand to the user
                

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    TotalPoints=0
    HandSize=calculate_handlen(hand)
    while HandSize>0:
            print('Current Hand: ')
            display_hand(hand)
            word=str(raw_input('Enter word, or a "." to indicate you are finished:'))
            if word==".":
                HandSize=0
                
            elif is_valid_word(word,hand,word_list):
                        points=get_word_score(word, calculate_handlen(hand))
                        hand=update_hand(hand,word)
                        TotalPoints=points+TotalPoints
                        print('"'+str(word)+'"' + ' earned ' + str(points) + ' points. Total: ' + str(TotalPoints))
            else:
                print('Not a valid word. Please try again.')
    
    print ('Total Score: ' + str(TotalPoints))
    return TotalPoints

##word_list=load_words()
##hand=deal_hand(7)
##points=play_hand(hand,word_list)
##print(points)

#
# Problem #5: Playing a game
# 

def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, ask them again.
 
    2) When done playing the hand, repeat from step 1    
    """
    # TO DO
    n=7 #n is equivalent to Hand_Size
    hand=deal_hand(n)
    End=0
    while End==0:
        input=raw_input('Input either "n" or "r" or "e":')
        if input=='n':
            hand=deal_hand(n)
            play_hand(hand,word_list)
        elif input=='r':
            play_hand(hand,word_list)
        elif input=='e':
            End=1
        else:
            print('Input cannot be recognized. Please try again.')
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
