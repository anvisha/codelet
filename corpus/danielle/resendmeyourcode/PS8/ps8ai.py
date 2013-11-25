# 6.00 Problem Set 8 Part A
#
# Name:Danielle Chow
# Collaborators:
# Time: 3:00


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
    
    NumViruses1 = [0 for i in range(numTrials)]
    
    NumViruses2 = [0 for i in range(numTrials)]
    
    NumViruses3 = [0 for i in range(numTrials)]
    
    NumViruses4 = [0 for i in range(numTrials)]
    

    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(numViruses)]
    for trial in range(numTrials):
        patient1 = TreatedPatient(viruses, maxPop)
        patient2 = TreatedPatient(viruses, maxPop)
        patient3 = TreatedPatient(viruses, maxPop)
        patient4 = TreatedPatient(viruses, maxPop)
                                
        for n in range(300):
            NumViruses1[trial] =(patient1.update())        
        for n in range(300, 450):
            NumViruses1[trial] = patient1.update()
        patient1.addPrescription('guttagonol')
        for n in range(450, 600):
            NumViruses1[trial] = patient1.update()

        
        for n in range(150):
            NumViruses2[trial] =(patient2.update())
       
        for n in range(150, 300):
            NumViruses2[trial] = patient2.update()
        patient2.addPrescription('guttagonol')
        for n in range(300, 450):
            NumViruses2[trial] = patient2.update()


            
        for n in range(75):
            NumViruses3[trial] =patient3.update()
        for n in range(75, 225):
            NumViruses3[trial] = patient3.update()
        patient3.addPrescription('guttagonol')
        for n in range(225, 375):
            NumViruses3[trial] = patient3.update()


        for n in range(150):
            NumViruses4[trial] =patient4.update()
        patient4.addPrescription('guttagonol')
        for n in range(150, 300):
            NumViruses4[trial] = patient4.update()
        

            
    

    pylab.subplot(221)
    pylab.hist(NumViruses1, bins = 20)
    xmin, xmax = pylab.xlim()
    pylab.suptitle('Virus Population with Drug Introduced at 300, 150, 75, 0 Day Delay')
    pylab.xlabel = ("Total Viruses with 300 time steps Before drug addition")
    pylab.ylabel = ("Number of Trials")

    pylab.subplot(222)
    pylab.hist(NumViruses2, bins = 20)
    xmin, xmax = pylab.xlim()
    pylab.xlabel = ("Total Viruses with 150 time steps Before drug addition")
    pylab.ylabel = ("Number of Trials")

    pylab.subplot(223)
    pylab.hist(NumViruses3, bins = 20)
    xmin, xmax = pylab.xlim()
    pylab.xlabel = ("Total Viruses with 75 time steps Before drug addition")
    pylab.ylabel = ("Number of Trials")

    pylab.subplot(224)
    pylab.hist(NumViruses4, bins = 20)
    xmin, xmax = pylab.xlim()
    pylab.xlabel = ("Total Viruses with 0 time steps Before drug addition")
    pylab.ylabel = ("Number of Trials")
                    

                    
    pylab.show()
