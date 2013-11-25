###########################
# Problem Set 9: Space Cows 
# Name: Danielle Chow
# Collaborators:Hilary Mullholland
# Time:2

import pylab

#============================
# Part A: Breeding Alien Cows
#============================

# Problem 1: File I/O
def loadData(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated x,y pairs.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    (x, y) - a tuple containing a Pylab array of x values and
             a Pylab array of y values
    """
    datafile = open(filename)
    datalist = [ line.rstrip() for line in datafile.readlines() ]
    x= [] #number of days
    y = [] #number of alien cows
    for line in datalist:
        for i in range(len(line)):
            if line[i] == ',':
                x.append(int(line[:i]))
                y.append(int(line[i+1:]))
            else:
                continue
    
    
    return (pylab.array(x), pylab.array(y)) #tuple containing a pylab arrays of x and y values
    

# Problem 2a: Curve Fitting: Finding a polynomial fit
def polyFit(x, y, degree):
    """
    Find the best fit polynomial curve z of the specified degree for the data
    contained in x and y and returns the expected y values for the best fit
    polynomial curve for the original set of x values.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values
    degree - the degree of the desired best fit polynomial

    Returns:
    z - a Pylab array of coefficients for the polynomial fit function of the
        specified degree, corresponding to the input domain x.
    """
    
   
        
    coefficients = pylab.polyfit(x, y, degree)
    array = pylab.array(coefficients)
    return array
    
    

# Problem 2b: Curve Fitting: Finding an exponential fit
def expFit(x, y):
    """
    Find the best fit exponential curve z for the data contained in x and y.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values

    Returns:
    z - a Pylab array of coefficients for the exponential fit function
        corresponding to the input domain x.
    """
    coefficients = polyFit( x, pylab.log2(y), 1)
    return coefficients
    
    
    


# Problem 3: Evaluating regression functions
def rSquare(measured, estimated):
    """
    Calculate the R-squared error term.

    Parameters:
    measured - one dimensional array of measured values
    estimate - one dimensional array of predicted values

    Returns: the R-squared error term
    """
    assert len(measured) == len(estimated)
    EE = ((estimated - measured)**2).sum()
    mMean = measured.sum()/float(len(measured))
    MV = ((mMean - measured)**2).sum()
    return 1 - EE/MV



def estimatedValuesLinear(xdata, linear_coefficients):
    a, b = linear_coefficients
    estimatedValues = a*xdata + b
    return estimatedValues
def estimatedValuesQuad(xdata, quadratic_coefficients):
    a, b, c = quadratic_coefficients
    estimatedValues = a*xdata**2 + b*xdata + c
    return estimatedValues
def estimatedValuesQuart(xdata, quartic_coefficients):
    a, b, c, d, e = quartic_coefficients
    estimatedValues = a*xdata**4 + b*xdata**3 + c*xdata**2 + d*xdata + e
    return estimatedValues
def estimatedValuesExp(xdata, exponential_coefficients):
    b, log_a = exponential_coefficients
    a = pylab.exp2(log_a)
    estimatedValues = a*pylab.exp2(b*xdata)
    return estimatedValues
#======================
# TESTING CODE
###======================
def main():
    # Problem 1
    data1 = loadData('ps9a_data1.txt')
    data2 = loadData('ps9a_data2.txt')
    data3 = loadData('ps9a_data3.txt')

    # Checks for Problem 1
    assert all( [len(data) == 25 for xy in data] for data in [data1, data2] ), \
        "Error loading data from files; number of terms does not match expected"
    assert all( [len(data) == 100 for xy in data] for data in [data1, data2] ), \
        "Error loading data from files; number of terms does not match expected"


    xdata1, ydata1 = data1
    xdata2, ydata2 = data2
    xdata3, ydata3 = data3

    data = [(xdata1, ydata1), (xdata2, ydata2), (xdata3, ydata3)]

    #coefficients for best fit curves
    linear_coefficients = polyFit(xdata1, ydata1,1)
    quadratic_coefficients = polyFit(xdata1, ydata1,2)
    quartic_coefficients = polyFit(xdata1, ydata1,4)
    exponential_coefficients = expFit(xdata1, ydata1)
    


    for each in data:
        plot(each[0], each[1], linear_coefficients, quadratic_coefficients, quartic_coefficients, exponential_coefficients)

        


def plot(xdata, ydata, linear_coefficients, quadratic_coefficients, quartic_coefficients, exponential_coefficients):

    
    pylab.subplot(221)
    pylab.scatter(xdata, ydata)
    pylab.plot(xdata, estimatedValuesLinear(xdata, linear_coefficients), label = 'linear' + ', R2 = ' + str(round(rSquare(ydata, estimatedValuesLinear(xdata, linear_coefficients)), 4)))
    pylab.xlabel('xdata')
    pylab.ylabel('estimated y values')
    pylab.legend()

    pylab.subplot(222)
    pylab.scatter(xdata, ydata)
    pylab.plot(xdata, estimatedValuesQuad(xdata, quadratic_coefficients), label = 'quadraticratic' + ', R2 = ' + str(round(rSquare(ydata, estimatedValuesQuad(xdata, quadratic_coefficients)), 4)))
    pylab.xlabel('xdata')
    pylab.ylabel('estimated y values')
    pylab.legend()

    pylab.subplot(223)
    pylab.scatter(xdata, ydata)
    pylab.plot(xdata, estimatedValuesQuart(xdata, quartic_coefficients), label = 'quartic' + ', R2 = ' + str(round(rSquare(ydata, estimatedValuesQuart(xdata, quartic_coefficients)),4)))
    pylab.xlabel('xdata')
    pylab.ylabel('estimated y values')
    pylab.legend()

    pylab.subplot(224)
    pylab.scatter(xdata, ydata)
    pylab.plot(xdata, estimatedValuesExp(xdata, exponential_coefficients), label = 'exponential' + ', R2 = ' + str(round(rSquare(ydata, estimatedValuesExp(xdata, exponential_coefficients)), 4)))
    pylab.xlabel('xdata')
    pylab.ylabel('estimated y values')
    pylab.legend()

    

    

    pylab.show()


if __name__ == "__main__":
    main()
