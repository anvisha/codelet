# 6.00 Problem Set 8 Part B
#
# Name:
# Collaborators:
# Time:



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
    def __init__(self, name, population, electoral_votes, dem_vote_share, rep_vote_share,\
                 marg_error):
        self.name=name
    #The following code outlines the attributes of the class    
        self.population=float(population)
        self.dem_vote_share=float(dem_vote_share)
        self.rep_vote_share=float(rep_vote_share)
        self.marg_error=float(marg_error)
        self.electoral_votes=float(electoral_votes)

    #This code extablished get functions for the attributes
    def get_name(self):
        return self.name
    def get_population(self):
        return self.population
    def get_dem_vote_share(self):
        return self.dem_vote_share
    def get_rep_vote_share(self):
        return self.rep_vote_share
    def get_marg_error(self):
        return self.marg_error
    def get_electoral_votes(self):
        return self.electoral_votes
    

    def getStandardError(self):
        """
        Returns Standard Error of the polling data
        for the state based on margin of Error 
        """
        #The standard error is calculated with the marginal error
        #and the 1.96 standard deviations(95% confidence)
        standard_error=float(self.get_marg_error())/float(1.96)
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
        SE=self.getStandardError()#calculatees standard error
        dem_perc=random.gauss(self.get_dem_vote_share(), SE)#gets democrat vote percentage
        rep_perc=random.gauss(self.get_rep_vote_share(), SE)#gets republican vote percentage
        if dem_perc>rep_perc:#sees If democrat received more votes
            #returns tuple with number of popular votes and give electoral votes
            #to the democrat
            tuples=[(self.get_electoral_votes(), (dem_perc/float(100))*self.get_population())\
                  ,(0,(rep_perc/float(100))*self.get_population())]
        else:
            #returns tuple with number of popular votes and gives the electoral
            #votes to republicans
            tuples=[(0, (dem_perc/100)*self.get_population())\
                  , (self.get_electoral_votes(),(rep_perc/float(100))*self.get_population())]

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
    rep_dist=[]
    rep_elec_tot=[]
    dem_elec_tot=[]
    rep_wins=[]
    dem_wins=[]
    ties=[]
    for x in range(numTrials):#iterates through loop for each trial
        #creates lists for use later
        dem_pop=[]
        rep_pop=[]
        rep_elec=[]
        dem_elec=[]
        for state in states:#iterates through states
            dem_pop.append(state.vote()[0][1])#records dem popular vote per state
            rep_pop.append(state.vote()[1][1])#records repub popular vote per state
            dem_elec.append(state.vote()[0][0])#records dem popular vote per state
            rep_elec.append(state.vote()[1][0])#records rep popular vote per state
        dem_elec_tot.append(sum(dem_elec))
        rep_elec_tot.append(sum(rep_elec))
        if sum(dem_elec)>sum(rep_elec):#if the democrats win, adds a win to their total
            dem_wins.append(1)
        elif sum(dem_elec)==sum(rep_elec):#if there is a tie, adds to the tie total
            ties.append(1)
        else:
            rep_wins.append(1)#if the republicans win, adds to their win total
    #computes average electoral votes for each candidate        
    rep_avg_votes=(sum(rep_elec_tot)/float(numTrials))
    dem_avg_votes=(sum(dem_elec_tot)/float(numTrials))
    #calculates the deviation from the mean for each data point
    for vote in rep_elec_tot:
        rep_dist.append((vote-rep_avg_votes)**2)
    #calculates standard deviation
    SD=(sum(rep_dist)/len(rep_dist))**.5
    #calculates confidence intervals
    conf_int_rep=[rep_avg_votes-1.96*SD, rep_avg_votes+1.96*SD]
    conf_int_dem=[dem_avg_votes-1.96*SD, dem_avg_votes+1.96*SD]
  
    print rep_avg_votes
    print dem_avg_votes
    print conf_int_rep
    print conf_int_dem
    print sum(rep_wins)
    print sum(dem_wins)
    print sum(ties)
    
    #plots the data as subplots and assigns titles
    pylab.subplot(1,2,1)
    pylab.title("Republican Electoral Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(rep_elec_tot, bins=10)
    

    pylab.subplot(1,2,2)
    pylab.title("Democratic Electoral Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(dem_elec_tot, bins=10)

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
    rep_dist=[]
    rep_pop_tot=[]
    dem_pop_tot=[]
    rep_wins=[]
    dem_wins=[]
    ties=[]
    for x in range(numTrials):
        dem_pop=[]
        rep_pop=[]
        rep_elec=[]
        dem_elec=[]
        for state in states:
            dem_pop.append(state.vote()[0][1])#records dem popular vote per state
            rep_pop.append(state.vote()[1][1])#records repub popular vote per state
            dem_elec.append(state.vote()[0][0])#records dem popular vote per state
            rep_elec.append(state.vote()[1][0])#records rep popular vote per state
        dem_pop_tot.append(sum(dem_pop))
        rep_pop_tot.append(sum(rep_pop))

        #determines and keeps track of which party wins the election
        if sum(dem_pop)>sum(rep_pop):
            dem_wins.append(1)
        elif sum(dem_pop)==sum(rep_pop):
            ties.append(1)
            
        else:
            rep_wins.append(1)
    #calculates average votes
    rep_avg_votes=(sum(rep_pop_tot)/float(numTrials))
    dem_avg_votes=(sum(dem_pop_tot)/float(numTrials))
    #
    #necessary calculations for standard deviation and confidence intervals
    for vote in rep_pop_tot:
        rep_dist.append((vote-rep_avg_votes)**2)
    SD=(sum(rep_dist)/len(rep_dist))**.5
    conf_int_rep=[rep_avg_votes-1.96*SD, rep_avg_votes+1.96*SD]
    conf_int_dem=[dem_avg_votes-1.96*SD, dem_avg_votes+1.96*SD]

    print rep_avg_votes
    print dem_avg_votes
    print conf_int_rep
    print conf_int_dem
    print sum(rep_wins)
    print sum(dem_wins)
    print sum(ties)

    #plots the data as subplots
    pylab.subplot(1,2,1)
    pylab.title("Republican Popular Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(rep_pop_tot, bins=10)
    

    pylab.subplot(1,2,2)
    pylab.title("Democratic Popular Vote")
    pylab.xlabel("Number of Votes")
    pylab.ylabel("Number of Trials")
    pylab.hist(dem_pop_tot, bins=10)

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
    rep_dist=[]
    rep_elec_tot=[]
    dem_elec_tot=[]
    dem_pop_tot=[]
    rep_pop_tot=[]
    rep_wins=[]
    dem_wins=[]
    pop_less_elec=0
    for x in range(numTrials):
        dem_pop=[]
        rep_pop=[]
        rep_elec=[]
        dem_elec=[]
        for state in states:
            dem_pop.append(state.vote()[0][1])#records dem popular vote per state
            rep_pop.append(state.vote()[1][1])#records repub popular vote per state
            dem_elec.append(state.vote()[0][0])#records dem popular vote per state
            rep_elec.append(state.vote()[1][0])#records rep popular vote per state
        dem_elec_tot.append(sum(dem_elec))#keeps track of electoral votes
        rep_elec_tot.append(sum(rep_elec))#keeps track of electoral votes
        dem_pop_tot.append(sum(dem_pop))#keeps track of popular votes
        rep_pop_tot.append(sum(rep_pop))#keeps track of popular votes
        #Keeps track of wins for each party and ties
        if sum(dem_elec)>sum(rep_elec):
            dem_wins.append(1)
        elif sum(dem_pop)==sum(rep_pop):
            ties.append(1)
        else:
            rep_wins.append(1)
        #checks if someone one without winning the popular vote and keeps track
        if sum(dem_elec)>sum(rep_elec)and sum(dem_pop)<sum(rep_pop):
            pop_less_elec+=1
        if sum(dem_elec)<sum(rep_elec)and sum(dem_pop)>sum(rep_pop):
            pop_less_elec+=1
    #prints requested values        
    print sum(rep_wins)
    print sum(dem_wins)
    print pop_less_elec




