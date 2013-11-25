# 6.00 Problem Set 8 Part A
#
# Name:
# Collaborators:
# Time:


import numpy
import random
import pylab
from ps7b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a list of drugs that each ResistantVirus is resistant to
                 (a list of strings, e.g., ['guttagonol'])
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    """
    num_viruses={}
    delays=[300,150,75,0]
    for delay in delays:
        virus_values=simulation(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials, delay)
        num_viruses[delay]=virus_values
        
    x=1
    for delay in delays:
        pylab.subplot(2,2,x)
        pylab.title("Drug With Delay: " + str(delay))
        pylab.xlabel("Virus Population")
        pylab.ylabel("Number of Trials")
        pylab.hist(num_viruses[delay], bins=10, range=(0, 10)) 
        x=x+1

    pylab.show()

def simulation(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials,delay):    
    virus_pop_tot=[]
    for j in range(numTrials):
        time_step=0
        virus_pop=[]
        resist_virus=[]
        viruses=[]
        #creates viruses and adds them to a list
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances,\
                                          mutProb))
        #creates patient
        patient1=TreatedPatient(viruses, maxPop)
        
        
    

        numTimeSteps=delay+150
        #checks if the viruses reproduce or mutate at each time step
        #and adds the drug at step 1550
        for x in range(numTimeSteps):
            if x==delay-1:
                patient1.addPrescription('guttagonol')
            virus_pop.append(patient1.update())
            resist_virus.append(patient1.getResistPop(['guttagonol']))

        virus_pop_tot.append(virus_pop[numTimeSteps-1])
        
    return virus_pop_tot


    

