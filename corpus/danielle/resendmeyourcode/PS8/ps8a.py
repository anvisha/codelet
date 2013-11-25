# 6.00 Problem Set 8 Part A
#
# Name:Danielle Chow
# Collaborators:Tiffany Hood, Sammy Khalifa, and Carolina Lopez=Trevino
# Time:3 (shouldn't have taken this long. Struggled with importing)


import numpy
import random
import pylab
from ps7b import *

#
# PROBLEM 1
#
#Began writing another function...didn't really work out well. Please disregard.
#
##def DrugDelay(delay):
##    viruses=[]
##    for i in range(100):
##        viruses.append(ResistantVirus(.1,.05,{'guttagonol':False},.005))
##    patient=TreatedPatient(viruses,1000)
##    Total=[]
##
##    for step in range(delay):
##        Total.append(patient.update())
##
##        patient.addPrescription('guttagonol')
##
##    for step in range(150):
##        Totasl.append(patient.update())
##
##    return Total[-1]

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
        VirusValues=simulation(numViruses,maxPop,maxBirthProb,clearProb,resistances,mutProb,numTrials,delay)
        num_viruses[delay]=VirusValues

    x=1
    for delay in delays:
        pylab.subplot(2,2,x)
        pylab.title("Delay: " + str(delay))
        pylab.xlabel("Virus Population")
        pylab.ylabel("Number of Trials")
        pylab.hist(num_viruses[delay], bins=10, range=(0, 10)) 
        x=x+1

    pylab.show()


def simulation(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials,delay):    
    TotalPopulation=[]
    for i in range(numTrials):
        TimeStep=0
        VirusPopulation=[]
        resist_virus=[]
        viruses=[]
        #creates viruses and adds them to a list
        for j in range(numViruses):
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
            VirusPopulation.append(patient1.update())
            resist_virus.append(patient1.getResistPop(['guttagonol']))

        TotalPopulation.append(VirusPopulation[numTimeSteps-1])
        
    return TotalPopulation
