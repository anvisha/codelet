# 6.00 Problem Set 8 Part B
#
# Name:Tiffany Hood
# Collaborators: Carolina Lopez-Trevino
# Time: 8:00
# 1 Late Day Used



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
    def __init__(self, state, population, electoral, demVote, repubVote, error):
        self.state = state
        self.population = float(population)
        self.demVote = float(demVote)
        self.repubVote = float(repubVote)
        self.electoral = float(electoral)
        self.error = float(error)
    def getState (self):
        return self.state
    def getPopulation(self):
        return self.population
    def getDemVote(self):
        return self.demVote
    def getRepubVote(self):
        return self.repubVote
    def getElectoral (self):
        return self.electoral
    def getError (self):
        return self.error
     


    def getStandardError(self):
        """
        Returns Standard Error of the polling data
        for the state based on margin of Error 
        """
        return self.error/1.96
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
        error = self.getStandardError()
        demVote = self.getDemVote()
        repubVote = self.getRepubVote()
        dem = random.gauss(demVote, error)
        repub = random.gauss(repubVote, error)
        if dem >= repub:
            m = dem
            dPopVote = self.getPopulation() * (m/100)
            rPopVote = self.getPopulation() * ((100-m)/100)
            dElecVote = self.getElectoral() 
            rElecVote = 0
        else:
            m = repub
            rPopVote = self.getPopulation() * (m/100)
            dPopVote = self.getPopulation() * ((100-m)/100)
            rElecVote = self.getElectoral() 
            dElecVote = 0
    
        rVote = (rElecVote, rPopVote)
        dVote = (dElecVote, dPopVote)
        return [dVote, rVote]
            
       
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
    dataFile = open(filename, "r")
    lines = []
    for line in dataFile.readlines():
        if len(line) == 0 or line[0] == '#':
            continue
        else:
            lines.append(line.strip())
    states = []
    for n in lines:
        state = n.split(',')
        stateObject = State(state[0], state[1], state[2], state[3], state[4], state[5])
        states.append(stateObject)
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
    
    electoralDem = []
    electoralRepub = []
    demWin = 0
    repubWin = 0
    tie = 0
    
    repubTot = 0
    demTot = 0
    
    for n in range(numTrials):
        demVote = 0
        repubVote = 0
        for state in states:
            votes = state.vote()
            demVote += votes [0] [0]
            repubVote += votes [1] [0]
        electoralDem.append(demVote)
        electoralRepub.append(repubVote)
    for n in range(numTrials):
        demTot += electoralDem[n]
        repubTot += electoralRepub[n]
        if electoralDem[n] < electoralRepub[n]:
            repubWin +=1
        if electoralDem[n] > electoralRepub[n]:
            demWin += 1
        if electoralDem[n] == electoralRepub[n]:
            tie += 1

    
    demAvg = demTot/numTrials
    repubAvg = repubTot/numTrials
    percentDem = (float(demWin)/float(numTrials))*100
    percentRepub = (float(repubWin)/float(numTrials)) * 100
    percentTie = (float(tie)/float(numTrials)) *100

    #Confidence Interval Calculation
    distMean = []
    totalDist = 0
    for votes in electoralDem:
        distMean.append((votes-demAvg)**2)
    for distances in distMean:
        totalDist+=distances
    standardDev = (totalDist/len(electoralDem))**.5
    confidenceDem = [demAvg-(1.96*standardDev), demAvg+(1.96*standardDev)]
    confidenceRepub = [repubAvg-(1.96*standardDev), repubAvg+(1.96*standardDev)]
    
    print 'Average number of Democratic Electoral Votes:', demAvg
    print 'Average number of Republican Electoral Votes:', repubAvg
    print 'Confidence interval for Democrats:', confidenceDem
    print 'Confidence interval for Republicans:', confidenceRepub
    print 'Percentage of times Democrats Win:', percentDem
    print 'Percentage of times Republicans Win:', percentRepub
    print 'Percentage of times there is a tie:', percentTie
    
                
    
    pylab.subplot(1,2,1)
    pylab.title = ("Democratic Electoral Votes")
    pylab.xlabel = ("Votes")
    pylab.ylabel = ("Tials")
    pylab.hist(electoralDem, bins = 20)

    pylab.subplot(1,2,2)
    pylab.title = ('Republican Electoral Votes')
    pylab.xlabel = ('Votes')
    pylab.ylabel = ('Trials')
    pylab.hist(electoralRepub, bins = 20)
    

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
    popDem = []
    popRepub = []
    demWin = 0
    repubWin = 0
    tie = 0
    
    repubTot = 0
    demTot = 0
    
    for n in range(numTrials):
        demVote = 0
        repubVote = 0
        for state in states:
            votes = state.vote()
            demVote += votes [0] [1]
            repubVote += votes [1] [1]
        popDem.append(demVote)
        popRepub.append(repubVote)
    for n in range(numTrials):
        demTot += popDem[n]
        repubTot += popRepub[n]
        if popDem[n] < popRepub[n]:
            repubWin +=1
        if popDem[n] > popRepub[n]:
            demWin += 1
        if popDem[n] == popRepub[n]:
            tie += 1

    
    demAvg = demTot/numTrials
    repubAvg = repubTot/numTrials
    percentDem = (float(demWin)/float(numTrials))*100
    percentRepub = (float(repubWin)/float(numTrials)) * 100
    percentTie = (float(tie)/float(numTrials)) *100

    #Confidence Interval Calculation
    distMean = []
    totalDist = 0
    for votes in popDem:
        distMean.append((votes-demAvg)**2)
    for distances in distMean:
        totalDist+=distances
    standardDev = (totalDist/len(popDem))**.5
    confidenceDem = [demAvg-(1.96*standardDev), demAvg+(1.96*standardDev)]
    confidenceRepub = [repubAvg-(1.96*standardDev), repubAvg+(1.96*standardDev)]
    
    print 'Average number of Democratic Popular Votes:', demAvg
    print 'Average number of Republican Popular Votes:', repubAvg
    print 'Confidence interval for Democrats:', confidenceDem
    print 'Confidence interval for Republicans:', confidenceRepub
    print 'Percentage of times Democrats Win:', percentDem
    print 'Percentage of times Republicans Win:', percentRepub
    print 'Percentage of times there is a tie:', percentTie
    
                
    
    pylab.subplot(1,2,1)
    pylab.title = ("Democratic Popular Votes")
    pylab.xlabel = ("Votes")
    pylab.ylabel = ("Tials")
    pylab.hist(popDem, bins = 20)

    pylab.subplot(1,2,2)
    pylab.title = ('Republican Popular Votes')
    pylab.xlabel = ('Votes')
    pylab.ylabel = ('Trials')
    pylab.hist(popRepub, bins = 20)
    

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
    popDem = []
    popRepub = []
    elecDem = []
    elecRepub = []
    notPop = 0
    demPopVote = 0
    repubPopVote = 0
    demElecVote = 0
    repubElecVote = 0
    
    for n in range(numTrials):
        demVote = 0
        repubVote = 0
        for state in states:
            votes = state.vote()
            demPopVote += votes [0] [1]
            repubPopVote += votes [1] [1]
            demElecVote += votes [0] [0]
            repubElecVote += votes [1] [0]
        popDem.append(demPopVote)
        popRepub.append(repubPopVote)
        elecDem.append(demElecVote)
        elecRepub.append(repubElecVote)
    for n in range(numTrials):
        if elecDem[n] < elecRepub[n] and (popDem[n] > popRepub[n] or popDem[n] == popRepub[n]):
            notPop +=1
        if elecDem[n] > elecRepub[n] and (popDem[n] < popRepub[n] or popDem[n] == popRepub[n]):
            notPop += 1
    noPlurality = (notPop/numTrials)*100
    return 'Percentage of times the popular vote does not win the election:', noPlurality
    


