""" Various misc funcs """

from math import fabs, exp, sqrt, sin, pi, cos, tan, acos, asin
import sys
from collections import deque

__author__  = "Martin De Kauwe"
__version__ = "1.0 (09.03.2011)"
__email__   = "mdekauwe@gmail.com"

def float_eq(arg1, arg2, tol=1E-14):
    """arg1 == arg2"""
    return fabs(arg1 - arg2) < tol + tol * fabs(arg2)
    
def float_ne(arg1, arg2, tol=1E-14):
    """arg1 != arg2"""
    return not float_eq(arg1, arg2)

def float_lt(arg1, arg2, tol=1E-14):
    """arg1 < arg2"""
    return arg2 - arg1 > fabs(arg1) * tol
    
def float_le(arg1, arg2, tol=1E-14):
    """arg1 <= arg2"""
    return float_lt(arg1, arg2)

def float_gt(arg1, arg2, tol=1E-14):
    """arg1 > arg2"""
    return arg1 - arg2 > fabs(arg1) * tol

def float_ge(arg1, arg2, tol=1E-14):
    """arg1 >= arg2"""
    return float_gt(arg1, arg2)

def day_length(doy, yr_days, latitude):
    """ Daylength in hours

    Eqns come from Leuning A4, A5 and A6, pg. 1196
    
    Reference:
    ----------
    Leuning et al (1995) Plant, Cell and Environment, 18, 1183-1200.
    
    Parameters:
    -----------
    doy : int
        day of year, 1=jan 1
    yr_days : int
        number of days in a year, 365 or 366
    latitude : float
        latitude [degrees]

    Returns:
    --------
    dayl : float
        daylength [hrs]

    """
    deg2rad = pi / 180.0
    latr = latitude * deg2rad
    sindec = -sin(23.5 * deg2rad) * cos(2.0 * pi * (doy + 10.0) / yr_days)
    a = sin(latr) * sindec
    b = cos(latr) * cos(asin(sindec))
    dayl = 12.0 * (1.0 + (2.0 / pi) * asin(a / b))
    
    return dayl

def clip(value, min=None, max=None):
    """clip(value [, min [, max]]) => value

    Return value clipped to the range [min, max] inclusive. If either
    min or max is None, no clipping is performed on that side.
    """
    if min is not None and value < min:
        value = min
    if max is not None and value > max:
        value = max
    return value    

def uniq(inlist): 
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques

def calculate_daylength(yr_days, latitude):
    """ wrapper to put the day length into a list """
    return [day_length(d+1, yr_days, latitude) for d in xrange(yr_days)]

def str2boolean(value):
    """ Take the string value and return the boolean value, check case etc..."""
    if value is True or value is False or value is 0 or value is 1:
        return value
    elif isinstance(value, basestring) and value: 
        if value.lower() in ['true', 't', '1']: return True
        elif value.lower() in ['false', 'f', '0']: return False
    else:  
        raise ValueError("%s is no recognized as a boolean value" % value)
    
class SimpleMovingAverage():
    def __init__(self, window_size, previous_state=None):
        assert window_size == int(window_size) and window_size > 0, \
            "window_size must be an integer >0"
        self.window_size = window_size
        self.data = deque()
        if previous_state is not None:
            for i in xrange(window_size):
                self.data.append(previous_state)
        
    def __call__(self, n):
        data = self.data
        data.append(n)    # appends on the right
        data_length = len(data)
        if data_length > self.window_size:
            data.popleft()
            data_length -= 1
        if data_length == 0:
            average = 0.0
        else:
            average = sum( data ) / data_length
 
        return average
    
    def reset_stream(self):
        self.data = deque()
 
if __name__ == '__main__':

    print float_eq(0.0, 0.0)
    
    print float_ge(2.1000001, 2.1000001)
    
    
    import math
    import random
    import matplotlib.pyplot as plt
    random.seed(5)
    data = []
    for i in xrange(100):
        data.append(math.sin(random.random()))
    
    sma = SimpleMovingAverage(window_size=3, previous_state=1.0)
    store = []
    for index, val in enumerate(data):
        avg = sma(val)
        store.append(avg)
        #if index == 20:
        #    sma.reset_stream()
        
        #if index == 40:
        #    sma.reset_stream()
        
    
    plt.plot(store, "b-")
    plt.plot(data, "ro")
    plt.show()