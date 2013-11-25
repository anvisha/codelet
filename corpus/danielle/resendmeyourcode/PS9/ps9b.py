###########################
# Problem Set 9b: Space Cows 
# Name: Danielle Chow
# Collaborators:Hilarry Mullholland and Sammy Khalifa
# Time: 3

from ps9b_partition import getPartitions
import time

#================================
# Part 2: Transporting Space Cows
#================================

# Problem 5
def loadCows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name, weight pairs
    """
    datafile = open(filename)
    datalist = [ line.rstrip() for line in datafile.readlines() ]
    dictionary = {}
    for line in datalist:
        for i in range(len(line)):
            if line[i] == ',':
                dictionary[line[:i]] = float(line[i+1:])   #takes everything before commma and makes it the key, takes everything after and makes it the value in the dictionary
            else:
                continue
    return dictionary
    

# Problem 6
class Cow(object): #creates a class of cows
    def __init__(self, name, weight):
        self.name = name
        self.weight = float(weight)
    def getName(self):
        return self.name
    def getWeight(self):
        return self.weight
    def __str__(self):
        return self.name
    
def getCows(dictionary): #makes a list of the cows form the cows in the dictionary
    Cows=[]
    for i in dictionary:
        Cows.append(Cow(i,float(dictionary[i])))
    return Cows

def singleTransport(CopyCows, limit):
    result=[]
    TotalWeight=0.0
    i=0
    cowsTransported=[]
    while TotalWeight < limit and i < len(CopyCows):
        if (TotalWeight + CopyCows[i].getWeight()) <= limit: 
            cowsTransported.append(CopyCows[i]) #Cow makes his/her way on to the transport list
            TotalWeight += CopyCows[i].getWeight() #weight gets added into the total
        i+=1
    return cowsTransported

def greedyTransport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via a greedy heuristic (always choose the heaviest cow to fill the
    remaining space).
    
    Parameters:
    cows - a dictionary of name (string), weight (float) pairs
    limit - weight limit of the spaceship
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    Cows=getCows(cows)
    CopyCows=sorted(Cows, reverse=True) #sorts the cows in order of weight
    total=[]

    while len(CopyCows)>0: #runs through all cows
        TransportedCows=[]
        Transported=singleTransport(CopyCows, limit)
        for cow in Transported:
            TransportedCows.append(cow.getName()) #adds name of the cow transported to the transported list
        total.append(TransportedCows)
        for cow in Transported:
            CopyCows.remove(cow) #removes cow after transport

    return total

# Problem 7
def bruteForceTransport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.
    
    Parameters:
    cows - a dictionary of name (string), weight (float) pairs
    limit - weight limit of the spaceship
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """     
    CowNames=cows.keys()
    possibilities=getPartitions(CowNames)
    SpecialList=cows.keys() #default to the speacial list if the cow must be transported separately
    CopyCows=cows.copy()
    InnerList=[]

    for choice in possibilities:
        InnerList=[]
        weight=0

        for parts in choice:
            for cow in parts:
                weight+=CopyCows[cow]

            if weight<= limit:
                InnerList.append(parts)
            else:
                InnerList=[]
                break
            weight=0

        if len(InnerList) != 0 and len(InnerList)<len(SpecialList):
            SpecialList=InnerList

    return SpecialList

# Problem 8
if __name__ == "__main__":

    """
    Using the data from ps9b_data.txt and the specified weight limit, run your
    greedyTransport and bruteForceTransport functions here. Print out the
    number of trips returned by each method, and how long each method takes
    to run in seconds.
    """
    cows=loadCows('ps9b_data.txt')
    limit=1

    greedy=greedyTransport(cows,limit)
    print 'Greedy Transport method takes:', len(greedy), 'trips'
    brute=bruteForceTransport(cows,limit)
    print 'Brute Force Transport method takes:', len(brute), 'trips'
    
    
    # Question: How do the results compare? Which ran faster?
    
##start = time.time() 
##greedy=greedyTransport(cows,limit)
##print 'Greedy Transport method takes:', len(greedy), 'trips'  
##end = time.time() 
##print end - start
##
##start = time.time() 
##brute=bruteForceTransport(cows,limit)
##print 'Brute Force Transport method takes:', len(brute), 'trips' 
##end = time.time() 
##print end - start
