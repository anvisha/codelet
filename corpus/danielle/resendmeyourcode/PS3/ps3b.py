# Problem Set 3B
# Name: Danielle Chow
# Collaborators (Discussion): Sammy Khalifa
# Collaborators (Identical Solution): 
# Time: 4:00
#Late Days:1
#
from ps3a import *
import time
from perm import *


#
#
# Problem #6: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
    Given a hand and a word_dict, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all possible 
    permutations of lengths 1 to HAND_SIZE.

    If all possible permutations are not in word_list, return None.

    hand: dictionary (string -> int)
    word_list: list (string)
    returns: string or None
    """
    # BEGIN PSEUDOCODE <-- Remove this comment when you code this function
    # Create an empty list to store all possible permutations of length 1 to HAND_SIZE

    # For all lengths from 1 to HAND_SIZE (including! HAND_SIZE):

        # Get the permutations of this length

        # And store the permutations in the list we initialized earlier
        #  (hint: don't overwrite the list - you want to add to it)


    # Create a new variable to store the maximum score seen so far (initially 0)

    # Create a new variable to store the best word seen so far (initially None)  


    # For each possible word permutation:

        # If the permutation is in the word list:

            # Get the word's score

            # If the word's score is larger than the maximum score seen so far:

                # Save the current score and the current word as the best found so far



    # return the best word seen

    #
    HAND_SIZE=calculate_handlen(hand)
    permutations=[]
    i=2
    j=0
    MaxScore=0
    BestWord=[]
    while i<=HAND_SIZE:
        k=0
        elements=get_perms(hand,int(i))
        lenele=len(elements)
        while k<lenele:
            permutations.append(elements[k])
            k=k+1
       
##        print(permutations)
##        print (i)
            
        i=i+1
    size=len(permutations)
    while j<size:
        word=permutations[j]
        if word in word_list:
            score=get_word_score(word,HAND_SIZE)
            if score>MaxScore:
                MaxScore=score
                BestWord=word
        j=j+1

    if BestWord==[]:
        BestWord='None'
##    print ('Max score: ' + str(MaxScore))
##    print ('Best word: ' + str(BestWord))
    return BestWord

##hand=deal_hand(7)
##word_list=load_words()
##
##
##comp_choose_word(hand,word_list)

##print (comp_choose_word(hand, word_list))        




# Problem #7: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
    Allows the computer to play the given hand, following the same procedure
    as play_hand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. comp_choose_word returns None).
 
    hand: dictionary (string -> int)
    word_list: list (string)
    """
    #
    n=calculate_handlen(hand)
    score=0
    word=[]
    hand1=update_hand(hand,'')
    while word is not 'None':
        print('Available letters')
        display_hand(hand1)
        word=comp_choose_word(hand1,word_list)
##        print('1')
        
        if word=='None':
            print('There are no possible guesses left!')
        elif is_valid_word(word,hand1,word_list):
            print ('Computer guesses: ' + str(word))
            hand1=update_hand(hand1,word)
            score=score+get_word_score(word,n)
##            print('2')
            print ('and scores: ' + str(score) + ' points')
        else:
            print ('The computer guessed an invalid word.')
    

#
# Problem #8: Playing a game
#
#
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using play_hand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using comp_play_hand.

    4) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    n=7
    hand=deal_hand(n)
    End=0
    Terminate=0
    while End==0:
        while Terminate==0:
            input=raw_input('Input either "n" or "r" or "e":')
            if input=='n':
                hand=deal_hand(n)
                Terminate=1
            elif input=='r':
                Terminate=1
            elif input=='e':
                End=1
                Terminate=1
            else:
                print('Input could not be recognized. Please try again.')
        if End==0:
            while Terminate==1:
                decision=raw_input('Input either "u" or "c": ')
                if decision=='u':
                    play_hand(hand, word_list)
                    Terminate=0
                elif decision=='c':
                    comp_play_hand(hand,word_list)
                    Terminate=0
                else:
                    print('Input could not be recognized. Please try again.')
    ##play_game(word_list)

        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    print "Goodbye!"
