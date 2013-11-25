# 6.00 Problem Set 2
#
# Successive Approximation: Newton's Method
#

def evaluate_poly(poly, x):
    """
    Computes the value of a polynomial function at given value x. Returns that
    value as a float.

    Example:
    >>> poly = [0.0, 0.0, 5.0, 9.3, 7.0]    # f(x) = 5x^2 + 9.3x^3 + 7x^4 
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 5(-13)^2 + 9.3(-13)^3 + 7(-13)^4 
    180339.9

    poly: list of numbers, length > 0
    x: number
    returns: float
    """
    #Length of list/range or powers
    length= len(poly)

    #
    i=0 #Initial Power
    solution=0 #Initial Answer
    while i<length: #Evaluates solution term by term
         solution=(x**i)*poly[i]+solution #Function #Spent 45 minutes before realizing that "^" =/= "**" :(
         i=i+1
    return float(solution)
    

def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function as a list of
    floats. If the derivative is 0, returns [0.0].

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> print compute_deriv(poly)        # 35^x + 9x^2 + 4x^3
    [0.0, 35.0, 9.0, 4.0]

    poly: list of numbers, length > 0
    returns: list of numbers (floats)
    """
    #
    length=len(poly)
    Derivative=[]
    i=1 #Initial Power (i=1 because the derivative of the first term will always be zero)
    while i<length: #Evaulates term by term
        Derivative.append(float(i*(poly[i])))
        i=i+1
    return Derivative




def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a list containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [0.80679075379635201, 8]
    >>> poly = [1, 9, 8]
    >>> x_0 = -3
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [-1.0000079170005467, 6]

    poly: list of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: list [float, int]
    """
    #
    length=len(poly) 
    i=0
    x_i=x_0     #Renames x_0 to reflect a chaging guess
    if length>1:    #Checks that the derivative of the polynomial is not 0.
        trial=evaluate_poly(poly,x_i)   #Finds value of function for x_i
        i=i+1
        while abs(trial)>epsilon:   #Checks whether the value of the funtion for x_i is close enough to 0 to be considered a root
            x_i=x_i-(evaluate_poly(poly,x_i)/evaluate_poly(compute_deriv(poly),x_i)) #Newtonian Method computes the next guess of x_i
            trial=evaluate_poly(poly,x_i)   #Finds value of function for x_i
            i=i+1
    return [float(x_i),int(i)]
                      

