# 6.00 Problem Set 4
#
# Part A- RECURSION
#
# Name          : Danielle Chow
# Collaborators : Tiffany Hood
# Time spent    : 2.5

#
# Problem 1: Recursive String Reversal
#
def reverse_string(string):
    """
    Given a string, recursively returns a reversed copy of the string.
    For example, if the string is 'abc', the function returns 'cba'.
    The only string operations you are allowed to use are indexing,
    slicing, and concatenation.
    
    string: a string
    returns: a reversed string
    """
    ###

    if string=='':  #Checks to make sure there is some sort of input
        return string
    else:
        return reverse_string(string[1:])+string[0] #Removes the first letter and moves it to the end of the string. Then Takes the new string (minus the first letter) and runs the function again.
#
# Problem 2: Srinian
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('srini', 'histrionic')
    True
    >>> x_ian('john', 'mahjong')
    False
    >>> x_ian('max', 'maxwell')
    True
    
    
    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    ###
    if x[0]==word[0]:   #Checks to see if the first two letters in each list are the same
        if len(x)<=1:   #Checks to make the sequence we wish to find in the string is actually a sequence
            return True
        else:
            if len(word)>1: #Removes the first letter of both the word and the sequence
                x=x[1:]
                word=word[1:]
                return x_ian(x,word)    #Runs the function again with the 'new' word and the 'new' sequence
    else:
        if len(word)<=1:    #If the end of the word has been reached without finding the sequence, it's obviously not there
            return False
        else:
            word=word[1:]
            return x_ian(x,word)

#
# Problem 3: Typewriter
#
def insert_newlines(text, line_length):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately. 
    """
    ###

    if len(text)<=line_length:      #Specifies that if the text is not longer than the line length, then the text can just be printed without worrying about new lines
        return text
    else:
        if text[line_length-1]==' ':    #If the suggested line length ends on a space in the text, a new line can be added without worrying about interrupting a word
           return text[0:line_length-1]+'\n'+insert_newlines(text[line_length:],line_length)    #The text is edited to reflec tthe new line
        else:
            return text[0]+insert_newlines(text[1:],line_length)    #If the suggested line length does not fall on a space, the that non-space-letter will be removed from the text and run through the function again
            
            

