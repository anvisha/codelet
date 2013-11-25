# 6.00 Problem Set 10 Fall 2012
#
# Name: Danielle Chow
# Collaborators:Nick Flores, Tiffany Hood
# Time spent:5-6

import pylab
import random
import time

'''
Begin helper code
'''
def printSubjects(subjects, sortOutput=True):
    """
    Pretty-prints a list of Subject instances using the __str__ method
    of the Subject class.

    Parameters:
    subjects: a list of Subject instances to be printed
    sortOutput: boolean that indicates whether the output should be sorted
    according to the lexicographic order of the subject names
    """
    if sortOutput:
        subjectCmp = lambda s1, s2: cmp(s1.getName(), s2.getName())
        sortedSubjects = sorted(subjects, cmp=subjectCmp)
    else:
        sortedSubjects = subjects
        
    print 'Course\tValue\tWork\tLottery\n======\t=====\t====\t===='
    totalValue, totalWork, numLotteried = 0, 0, 0
    for subject in sortedSubjects:
        print subject
        totalValue += subject.getValue()
        totalWork += subject.getWork()
        numLotteried += subject.getLottery()

    print '\nNumber of subjects: %d\nTotal value: %d\nTotal work: %d \nTotal number of lottery subjects: %i \n' % \
          (len(subjects), totalValue, totalWork, numLotteried)
'''
End Helper Code
'''

class Subject(object):
    """
    A class that represents a subject.
    """
    def __init__(self, name, value, work, lottery):
        """
        Initializes a Subject instance.

        Parameters:
        name: a string that represents the name of the subject
        value: an integer that represents the value for the subject
        work: an integer that represents the amount of work for the subject
        lottery: a binary integer represents if this subject is lottery based
        """
        #attributes of the class
        self.name=name
        self.value=int(value)
        self.work=int(work)
        self.lottery=int(lottery)
        
    def getName(self):
        """
        Gets the name of the subject.

        Returns: a string that represents the name of the subject
        """
        return self.name
    
    def getValue(self):
        """
        Gets the value of the subject.
        
        Returns: an integer that represents the value of the subject
        """
        return int(self.value)

    def getWork(self):
        """
        Gets the amount of work for the subject.

        Returns: an integer that represents the work amount of the subject
        """
        return int(self.work)

    def getLottery(self):
        """
        Gets 1 if the subject is a lottery or 0 otherwise.

        Returns: a binary integer that represents if the subject is a lottery
        """
        return int(self.lottery)

    def __str__(self):
        """
        Generates the string representation of the Subject class.

        Returns:
        a string of the form <subject name>\t<value>\t<work>\t<lottery>
        where \t is the tab character
        """
        return  '%s\t%s\t%s\t%s' % (self.name, self.value, self.work,
                                   self.lottery)


def loadSubjects(filename):
    """
    Loads in the subjects contained in the given file. Assumes each line of
    the file
    is of the form "<subject name>,<value>,<work>,<lottery>" where
    each field is separated by a comma.

    Parameter:
    filename: name of the data file as a string

    Returns:
    a list of Subject instances, each representing one line from the data file
    """
    subjects=[]
    datalist= open(filename, "r")#opens file
    for line in datalist:
        subject_list = line.split(",")#splits the line at the comma
        #creates subject objects and adds them to a list
        subject=Subject(subject_list[0],subject_list[1],subject_list[2],subject_list[3])
        subjects.append(subject)
    return subjects

class SubjectAdvisor(object):
    """
    An abstract class that represents all subject advisors.
    """
    
    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick a set of subjects from the subjects list such that the value of
        the picked set is maximized, with the constraint that the total amount
        of work of the picked set needs to be <= maxWork and the total mount of
        lotteries subjects is <=maxLottery. To be implemented by subclasses.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """
        raise NotImplementedError('Should not call SubjectAdvisor.pickSubjects!')

    def getName(self):
        """
        Gets the name of the advisor. Useful for generating plot legends. To be
        implemented by subclasses.

        Returns:
        A string that represents the name of this advisor
        """
        raise NotImplementedError('Should not call SubjectAdvisor.getName!')


def cmpValue(subject1, subject2):
    """
    A comparator function for two subjects based on their values. To be used
    by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has more value than subject2, 1 if subject1 has less value
    than subject2, 0 otherwise
    """
    #calls the cmp function and compares values
    return cmp(subject2.getValue(), subject1.getValue())

def cmpWork(subject1, subject2):
    """
    A comparator function for two subjects based on their amount of work.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has less work than subject2, 1 if subject1 has more work
    than subject2, 0 otherwise
    """
    #calls the cmp function and compares work
    return cmp(subject1.getWork(), subject2.getWork())

def cmpRatio(subject1, subject2):
    """
    A comparator function for two subjects based on their value to work ratio.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has higher value to work ratio than subject2, 1 if subject1
    has lower value to work ratio than subject1, 0 otherwise
    """
    #calls the cmp function and compares ratios
    return cmp(float(subject2.getValue()) / subject2.getWork(),
               float(subject1.getValue()) / subject1.getWork())

class GreedyAdvisor(SubjectAdvisor):
    """
    An advisor that picks subjects based on a greedy algorithm.
    """
    
    def __init__(self, comparator):
        """
        Initializes a GreedyAdvisor instance.

        Parameter:
        comparator: a comparator function, either one of cmpValue, cmpWork,
                    or cmpRatio
        """
        #defines the subclass of subject advisor
        SubjectAdvisor.__init__(self)
        self.comp = comparator

    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Picks subjects to take from the subjects list using a greedy algorithm,
        based on the comparator function that is passed in during
        initialization.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lotteried subjects a student can take

        Returns:
        a list of Subject instances that are chosen to take
        """
        #sorts subjects 
        sortedSubjects = sorted(subjects, self.comp)
        #sets lists for later use
        work=[]
        currentSubjects=[]
        lotterySubjects=0
        
        
        for subject in subjects:
            #adds subject if it is below the work limit and not a lottery subject
            if (sum(work) + subject.getWork())<maxWork and subject.getLottery()==0:
                work.append(subject.getWork())
                currentSubjects.append(subject)
            #adds subject to current if it is below both the work and lottery limity
            elif (sum(work) + subject.getWork())<maxWork and subject.getLottery()==1:
                    if lotterySubjects< maxLottery:
                        lotterySubjects+=1
                        work.append(subject.getWork())
                        currentSubjects.append(subject)

        return currentSubjects
                

    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Greedy"

class BruteForceAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a BruteForceAdvisor instance.
        """
        #defines the subclass of subject advisor
        SubjectAdvisor.__init__(self)
        
    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick subjects to take using brute force. Use recursive backtracking
        while exploring the list of subjects in order to cut down the number
        of paths to explore, rather than exhaustive enumeration
        that evaluates every possible list of subjects from the power set.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """
        value, classes = self.helper(subjects[:], maxWork,maxLottery, [])
        return list(classes)

    def helper(self, subjectsLeft, workAvail,lotteryAvail, taken):
        if subjectsLeft == [] or workAvail == 0:
            result = (0,())
        elif subjectsLeft[0].getWork() > workAvail or lotteryAvail-subjectsLeft[0].getLottery()<0:
            result = self.helper(subjectsLeft[1:],workAvail,lotteryAvail, taken)
        else:
            subject = subjectsLeft[0]
            #This code adds the class to the subject and then continues
            withVal, withToTake = self.helper(subjectsLeft[1:],
                                         workAvail - subject.getWork(), lotteryAvail-subject.getLottery(),
                                         taken + [subject])
            withVal += subject.getValue()
            #This code doesn't take the class and checks to see what happens
            withoutVal, withoutToTake = self.helper(subjectsLeft[1:],workAvail,lotteryAvail, taken)
            #This class evaluates whether value is maximized with the class or without it
            if withVal > withoutVal :
                result = (withVal, withToTake + (subject,))
            else:
                result = (withoutVal, withoutToTake)

        return result
    
    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Brute Force"

class MemoizingAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a MemoizingAdvisor instance.
        """
        SubjectAdvisor.__init__(self)

    def pickSubjects(self, subjects, maxWork, maxLottery):
        """
        Pick subjects to take using memoization. Similar to
        BruteForceAdvisor except that the intermediate results are
        saved in order to avoid re-computation of previously traversed
        subject lists.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on
        maxLottery: maximum number of lottery subjects student is allowed to take.

        Returns:
        a list of Subject instances that are chosen to take
        """
        val,classes=self.helper(subjects[:],maxWork, (), maxLottery, None)
        return list(classes)

    def helper(self, subjectsLeft,workAvail, taken, lotteryAvail, memo):
        #creates dictionary 
        if memo==None:
            memo={}
        #problems keeps track of problem variables to store for later
        problems=(len(subjectsLeft), workAvail, lotteryAvail)
        #if the problem with specific parameters has been encountered before it brings the solution up from the  dictionary
        if problems in memo:
            result=memo[problems]
            return result
        #Basically the same as the brute force advisor
        if subjectsLeft == [] or workAvail == 0:
            result = (0,())
        elif subjectsLeft[0].getWork() > workAvail or lotteryAvail-subjectsLeft[0].getLottery()<0:
            result = self.helper(subjectsLeft[1:],workAvail,taken,lotteryAvail, memo)
       
        else:
            subject = subjectsLeft[0]
            #This code adds the class to the subject and continues 
            withClass, classestaken = self.helper(subjectsLeft[1:],workAvail - subject.getWork(),taken+(subject,), lotteryAvail-subject.getLottery(),memo)
            withClass += subject.getValue()
            #This code doesn't take the class and sees what happens
            withoutClass, withoutClass_classes = self.helper(subjectsLeft[1:],workAvail,taken,lotteryAvail, memo)
            #This class evaluates whether value is maximized with the class
            #or without it
            if withClass > withoutClass :
                result = (withClass, classestaken + (subject,))
            else:
                result = (withoutClass, withoutClass_classes)

        return result

        memo[problems]=result

    def getName(self):
        """
        Gets the name of the advisor.

        Returns:
        A string that represents the name of this advisor
        """
        return "Memoizing"


def measureTimes(filename, maxWork, maxLottery, subjectSizes, numRuns):
    """
    Compare the time taken to pick subjects for each of the advisors
    subject to maxWork constraint. Run different trials using different number
    of subjects as given in subjectSizes, using the subjects as loaded
    from filename. Choose a random subject of subjects for each trial.
    For instance, if subjectSizes is the list [10, 20, 30], then you should
    first select 10 random subjects from the loaded subjects, then run them
    through the three advisors using maxWork and maxLottery for numRuns times,
    measuring the time taken for each run, then average over the numRuns runs. After that,
    pick another set of 20 random subjects from the loaded subjects,
    and run them through the advisors, etc. Produce a plot afterwards
    with the x-axis showing number of subjects used, and y-axis showing
    time. Be sure you label your plots.

    After plotting the results, answer this question:
    What trend do you observe among the three advisors?
    How does the time taken to pick subjects grow as the number of subject
    used increases? Why do you think that is the case? Include the answers
    to these questions in your writeup.
    """
    subjects = loadSubjects(filename)

    advisors = [GreedyAdvisor(cmpRatio), BruteForceAdvisor(),
                MemoizingAdvisor()]
    advisorTimes = {}

    #creates dictionary with advisors as keys
    for advisor in advisors:
        advisorTimes[advisor] = []

    for size in subjectSizes:

        subjectsToUse = []
        for i in range(numRuns):
            sampleSubjects = random.sample(subjects, size)
            subjectsToUse.append(sampleSubjects)
        
        for advisor in advisors:
            total = 0.0
            for i in range(numRuns):
                sampleSubjects = subjectsToUse[i]
                #starts the time
                start = time.time()
                r = advisor.pickSubjects(sampleSubjects, maxWork, maxLottery)
                #calculates the time it took to run the code
                run_time = (time.time() - start)
                total += run_time
            #adds the times taken for each advisor to the dictionary
            #to be used for graphing later
            advisorTimes[advisor].append(total / numRuns)


    pylab.figure()
    for (advisor, times) in advisorTimes.iteritems():
        pylab.plot(subjectSizes, times, label = advisor.getName())

    pylab.title('Advisor Times')
    pylab.ylabel('Time elapsed')
    pylab.xlabel('Subject List Size')
    pylab.legend(loc = 'best')
    pylab.show()
            
