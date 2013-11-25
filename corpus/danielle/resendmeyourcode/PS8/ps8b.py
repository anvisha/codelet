# 6.00 Problem Set 8 Part B
#
# Name:Danielle Chow
# Collaborators:Tiffany Hood Sammy Khalifa
# Time:~6



import random
import string
import numpy
import pylab

#==========================================
# Problem Set 8 Part B: Elections Simulation
#==========================================

#
# Problem 2: US State Class
#
class State(object):
    ##TODO: class constructor, attributes, method 
    def __init__(self, name, population, electoralVotes, democraticVotes, republicanVotes,\
                 error):
        self.name=name
    #The following code outlines the attributes of the class    
        self.population=float(population)
        self.democraticVotes=float(democraticVotes)
        self.republicanVotes=float(republicanVotes)
        self.error=float(error)
        self.electoralVotes=float(electoralVotes)

    #This code extablished get functions for the attributes
    def get_name(self):
        return self.name
    def get_population(self):
        return self.population
    def get_democraticVotes(self):
        return self.democraticVotes
    def get_republicanVotes(self):
        return self.republicanVotes
    def get_error(self):
        return self.error
    def get_electoralVotes(self):
        return self.electoralVotes
    

    def getStandardError(self):
        """
        Returns Standard Error of the polling data
        for the state based on margin of Error 
        """
        #The standard error is calculated with the marginal error
        #and the 1.96 standard deviations(95% confidence)
        standard_error=float(self.get_error())/float(1.96)
        return standard_error

    #        
    # Problem 4: Vote!
    #    
    def vote(self):
        """
        Simulates a vote for the state
        based on the state asttributes.
        It will return a list of two tuples.
        The first tuple comprises of two values, the first values
        is the number of electoral votes, and the second value is
        the number of votes, for the Democratic candidate.
        The second tuple will comprise of the same two values
        for the Republican candidate.
        """
        CalcSE=self.getStandardError()#calculatees standard error
        democraticPercentage=random.gauss(self.get_democraticVotes(), CalcSE)#gets democrat vote percentage
        republicanPercentage=random.gauss(self.get_republicanVotes(), CalcSE)#gets republican vote percentage
        if democraticPercentage>republicanPercentage:#sees If democrat received more votes
            #returns tuple with number of popular votes and give electoral votes
            #to the democrat
            tuples=[(self.get_electoralVotes(), (democraticPercentage/float(100))*self.get_population())\
                  ,(0,(republicanPercentage/float(100))*self.get_population())]
        else:
            #returns tuple with number of popular votes and gives the electoral
            #votes to republicans
            tuples=[(0, (democraticPercentage/100)*self.get_population())\
                  , (self.get_electoralVotes(),(republicanPercentage/float(100))*self.get_population())]

        return tuples
        
       
#        
# Problem 3: Create States!
#
def createStates(filename):
    """
    Reads the textfile name 'filename',
    Creates an instance of a State object for each State in the file
    Return a list of the 51 State objects
    """
    # Here's some code that we give you to read in
    # the data and eliminate blank lines and comments.
    # The lines variable has a list of each line in the file.
    states=[]
    dataFile = open(filename, "r")
    lines = []
    for line in dataFile.readlines():
        if len(line) == 0 or line[0] == '#':
            continue
        else:
            lines.append(line.strip())
    #goes through each line of the excel file
    for entry in lines:
        state=entry.split(',')#splits the lines into elements in a list
        #returns the state object with the necessary inputs taken from
        #the excel file
        newState=State(state[0],state[1],state[2],state[3],state[4],state[5])
        states.append(newState)#adds new state to a list
    return states


        
        
            



    

##############
# Simulations
##############

#
# Problem 5:
#
def simulateElectoralVotes(numTrials, states):
    """
    Preforms an election simulation numTrials times for all the states in the country.
    Plots distribution of total electoral votes for each candidate
    Calculates average electoral votes for each candidate.
    Calculates confidence interval on the average number of electoral votes.
    Calculates percentage of times each candidate wins (or ties) by electoral votes
    """
    #creates lists to be used later
    republicanDistribution=[]
    republicanElectoralTotal=[]
    democraticElectoralTotal=[]
    republicanWins=[]
    democraticWins=[]
    ties=[]
    for x in range(numTrials):#iterates through loop for each trial
        #creates lists for use later
        democraticPopular=[]
        republicanPopular=[]
        republicanElectoral=[]
        democraticElectoral=[]
        for state in states:#iterates through states
            democraticPopular.append(state.vote()[0][1])#records dem popular vote per state
            republicanPopular.append(state.vote()[1][1])#records repub popular vote per state
            democraticElectoral.append(state.vote()[0][0])#records dem popular vote per state
            republicanElectoral.append(state.vote()[1][0])#records rep popular vote per state
        democraticElectoralTotal.append(sum(democraticElectoral))
        republicanElectoralTotal.append(sum(republicanElectoral))
        if sum(democraticElectoral)>sum(republicanElectoral):#if the democrats win, adds a win to their total
            democraticWins.append(1)
        elif sum(democraticElectoral)==sum(republicanElectoral):#if there is a tie, adds to the tie total
            ties.append(1)
        else:
            republicanWins.append(1)#if the republicans win, adds to their win total
    #computes average electoral votes for each candidate        
    rep_avg_votes=(sum(republicanElectoralTotal)/float(numTrials))
    dem_avg_votes=(sum(democraticElectoralTotal)/float(numTrials))
    #calculates the deviation from the mean for each data point
    for vote in republicanElectoralTotal:
        republicanDistribution.append((vote-rep_avg_votes)**2)
    #calculates standard deviation
    SD=(sum(republicanDistribution)/len(republicanDistribution))**.5
    #calculates confidence intervals
    conf_int_rep=[rep_avg_votes-1.96*SD, rep_avg_votes+1.96*SD]
    conf_int_dem=[dem_avg_votes-1.96*SD, dem_avg_votes+1.96*SD]
  
    print rep_avg_votes
    print dem_avg_votes
    print conf_int_rep
    print conf_int_dem
    print sum(republicanWins)
    print sum(democraticWins)
    print sum(ties)
    
    #plots the data as subplots and assigns titles
    pylab.subplot(1,2,1)
    pylab.title("Republican Electoral Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(republicanElectoralTotal, bins=10)
    

    pylab.subplot(1,2,2)
    pylab.title("Democratic Electoral Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(democraticElectoralTotal, bins=10)

    pylab.show()
  

        
            
        

#    
# Problem 6:
#
def simulatePopularVotes(numTrials, states):
    """
    Preforms an election simulation  numTrials times for all the states in the country.
    Plots distribution of total actual votes for each candidate
    Calculates average actual votes for each candidate.
    Calculates confidence interval on the average number of votes.
    Calculates percentage of times each candidate wins (or ties) by popular votes
    """
    population=0
    republicanDistribution=[]
    republicanPopularTotal=[]
    democraticPopularTotal=[]
    republicanWins=[]
    democraticWins=[]
    ties=[]
    for x in range(numTrials):
        democraticPopular=[]
        republicanPopular=[]
        republicanElectoral=[]
        democraticElectoral=[]
        for state in states:
            democraticPopular.append(state.vote()[0][1])#records dem popular vote per state
            republicanPopular.append(state.vote()[1][1])#records repub popular vote per state
            democraticElectoral.append(state.vote()[0][0])#records dem popular vote per state
            republicanElectoral.append(state.vote()[1][0])#records rep popular vote per state
        democraticPopularTotal.append(sum(democraticPopular))
        republicanPopularTotal.append(sum(republicanPopular))

        #determines and keeps track of which party wins the election
        if sum(democraticPopular)>sum(republicanPopular):
            democraticWins.append(1)
        elif sum(democraticPopular)==sum(republicanPopular):
            ties.append(1)
            
        else:
            republicanWins.append(1)
    #calculates average votes
    rep_avg_votes=(sum(republicanPopularTotal)/float(numTrials))
    dem_avg_votes=(sum(democraticPopularTotal)/float(numTrials))
    #
    #necessary calculations for standard deviation and confidence intervals
    for vote in republicanPopularTotal:
        republicanDistribution.append((vote-rep_avg_votes)**2)
    SD=(sum(republicanDistribution)/len(republicanDistribution))**.5
    conf_int_rep=[rep_avg_votes-1.96*SD, rep_avg_votes+1.96*SD]
    conf_int_dem=[dem_avg_votes-1.96*SD, dem_avg_votes+1.96*SD]

    print rep_avg_votes
    print dem_avg_votes
    print conf_int_rep
    print conf_int_dem
    print sum(republicanWins)
    print sum(democraticWins)
    print sum(ties)

    #plots the data as subplots
    pylab.subplot(1,2,1)
    pylab.title("Republican Popular Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(republicanPopularTotal, bins=10)
    

    pylab.subplot(1,2,2)
    pylab.title("Democratic Popular Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(democraticPopularTotal, bins=10)

    pylab.show()
    
    
#    
# Problem 7:
#
def simulatePlurality(numTrials, states):
    """
    Preforms an election simulation for all the states in the country.
    Calculate percentage of times the winning candidate (by electoral votes)
    does not win by popular vote.
    """
    population=0
    republicanDistribution=[]
    republicanElectoralTotal=[]
    democraticElectoralTotal=[]
    democraticPopularTotal=[]
    republicanPopularTotal=[]
    republicanWins=[]
    democraticWins=[]
    election=0
    for x in range(numTrials):
        democraticPopular=[]
        republicanPopular=[]
        republicanElectoral=[]
        democraticElectoral=[]
        for state in states:
            democraticPopular.append(state.vote()[0][1])#records dem popular vote per state
            republicanPopular.append(state.vote()[1][1])#records repub popular vote per state
            democraticElectoral.append(state.vote()[0][0])#records dem popular vote per state
            republicanElectoral.append(state.vote()[1][0])#records rep popular vote per state
        democraticElectoralTotal.append(sum(democraticElectoral))#keeps track of electoral votes
        republicanElectoralTotal.append(sum(republicanElectoral))#keeps track of electoral votes
        democraticPopularTotal.append(sum(democraticPopular))#keeps track of popular votes
        republicanPopularTotal.append(sum(republicanPopular))#keeps track of popular votes
        #Keeps track of wins for each party and ties
        if sum(democraticElectoral)>sum(republicanElectoral):
            democraticWins.append(1)
        elif sum(democraticPopular)==sum(republicanPopular):
            ties.append(1)
        else:
            republicanWins.append(1)
        #checks if someone one without winning the popular vote and keeps track
        if sum(democraticElectoral)>sum(republicanElectoral)and sum(democraticPopular)<sum(republicanPopular):
            election+=1
        if sum(democraticElectoral)<sum(republicanElectoral)and sum(democraticPopular)>sum(republicanPopular):
            election+=1
    #prints requested values        
    print sum(republicanWins)
    print sum(democraticWins)
    print election




