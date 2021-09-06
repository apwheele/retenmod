'''
Model functions to estimate
various retention models

Motivation taken from R foretell package
https://cran.r-project.org/web/packages/foretell/foretell.pdf

And paper How to Project Customer Retention” Revisited 
https://www.sciencedirect.com/science/article/pii/S1094996818300057

Andy Wheeler
'''

from collections import namedtuple
from scipy.optimize import minimize
from scipy.special import beta
import numpy as np

# Named tuple using for each of my functions output
churnmod = namedtuple("churnmod",["proj","negLL","params"])

# Should maybe write a helper to curry the models
# Given a log-ll and forecasting function

# Function for DbW model
def bdw(sval,h,bnds=[(0.001,10000)]*3,start=[1,1,1]):
    """Fits BdW retention model
    
    Keyword arguments:
    s : array, historical retention rates on scale of 0-100 should start at 100
    h : int, how many forecast periods to make
    bnds : list, tuples of lower/upper bounds for parameters
    start: list, starting values for optimization

    Returns:
    res: namedtuple, elements projected, loglikelihood, and parameters
                     if failed returns -1
    """
    surv = np.array(sval) #coercing to np array
    if surv[0] != 100:
        print(f'Starting value should be 100, current is surv[0]')
        return -1
    elif (surv.max() > 100.0) | (surv.min() < 0.0):
        print('No values should be above 100 or below 0')
        return -1
    t = len(surv)
    die = np.diff(-surv)
    i = np.arange(t)
    # log-likelihood function with respect to data
    def bdw_ll(x):
        a,b,c = x
        s = beta(a,b + i**c)/beta(a,b)
        p = np.diff(-s)
        ll_ = die * np.log(p)
        ll = ll_.sum() + surv[-1]*np.log(s[-1])
        return -ll
    res = minimize(bdw_ll,x0=start,method='L-BFGS-B',bounds=bnds)
    if res.success is not True:
        print('L-BFGS-B fitting failed, trying SLSQP')
        res = minimize(bdw_ll,x0=start,method='SLSQP',bounds=bnds)
    if res.success:
        # Projecting out multiple values
        a,b,c = res.x
        k = np.arange(0,t+h)
        proj_val = (beta(a,b+k**c)/beta(a,b))*100
        res_tup = churnmod(proj_val,res.fun,res.x)
        return res_tup
    else:
       print('Optimization not successful')
       print(res)
       return -1

# Function for BG model
def bg(sval,h,bnds=[(0.001,10000)]*2,start=[1,2]):
    """Fits BG retention model
    
    Keyword arguments:
    s : array, historical retention rates on scale of 0-100 should start at 100
    h : int, how many forecast periods to make
    bnds : list, tuples of lower/upper bounds for parameters
    start: list, starting values for optimization

    Returns:
    res: namedtuple, elements projected, loglikelihood, and parameters
                     if failed returns -1
    """
    surv = np.array(sval) #coercing to np array
    if surv[0] != 100:
        print(f'Starting value should be 100, current is surv[0]')
        return -1
    elif (surv.max() > 100.0) | (surv.min() < 0.0):
        print('No values should be above 100 or below 0')
        return -1
    t = len(surv)
    die = np.diff(-surv)
    i = np.arange(t)
    # log-likelihood function with respect to data
    def db_ll(x):
        a,b = x
        s = beta(a,b + i)/beta(a,b)
        p = np.diff(-s)
        ll_ = die * np.log(p)
        ll = ll_.sum() + surv[-1]*np.log(s[-1])
        return -ll
    res = minimize(db_ll,x0=start,method='L-BFGS-B',bounds=bnds)
    if res.success is not True:
        print('L-BFGS-B fitting failed, trying SLSQP')
        res = minimize(db_ll,x0=start,method='SLSQP',bounds=bnds)
    if res.success:
        # Projecting out multiple values
        a,b = res.x
        k = np.arange(0,t+h)
        proj_val = (beta(a,b+k)/beta(a,b))*100
        res_tup = churnmod(proj_val,res.fun,res.x)
        return res_tup
    else:
       print('Optimization not successful')
       print(res)
       return -1

# Function for LCW model
def lcw(sval,h,
        bnds=[(0.001,0.999),(0.001,10000),(0.001,0.999),(0.001,10000),(0.001,0.999)],
        start=[0.5, 2, 0.5, 1, 0.6]):
    """Fits LCW retention model
    
    Keyword arguments:
    s : array, historical retention rates on scale of 0-100 should start at 100
    h : int, how many forecast periods to make
    bnds : list, tuples of lower/upper bounds for parameters
    start: list, starting values for optimization

    Returns:
    res: namedtuple, elements projected, loglikelihood, and parameters
                     if failed returns -1
    """
    surv = np.array(sval) #coercing to np array
    if surv[0] != 100:
        print(f'Starting value should be 100, current is surv[0]')
        return -1
    elif (surv.max() > 100.0) | (surv.min() < 0.0):
        print('No values should be above 100 or below 0')
        return -1
    t = len(surv)
    die = np.diff(-surv)
    i = np.arange(t)
    # log-likelihood function with respect to data
    def lcw_ll(x):
        t1,c1,t2,c2,w = x
        s = w*(1-t1)**(i**c1) + (1-w)*(1-t2)**(i**c2)
        p = np.diff(-s)
        ll_ = die * np.log(p)
        ll = ll_.sum() + surv[-1]*np.log(s[-1])
        return -ll
    res = minimize(lcw_ll,x0=start,method='L-BFGS-B',bounds=bnds)
    if res.success is not True:
        print('L-BFGS-B fitting failed, trying SLSQP')
        res = minimize(lcw_ll,x0=start,method='SLSQP',bounds=bnds)
    if res.success:
        # Projecting out multiple values
        t1,c1,t2,c2,w = res.x
        k = np.arange(0,t+h)
        proj_val = (w*(1-t1)**(k**c1) + (1-w)*(1-t2)**(k**c2))*100
        res_tup = churnmod(proj_val,res.fun,res.x)
        return res_tup
    else:
       print('Optimization not successful')
       print(res)
       return -1

## Very simple use case, copied from R foretell library
#surv_val = [100,86.9,74.3,65.3,59.3]
#bdw(surv_val,5)
#bg(surv_val,5)
## LCW needs more values to fit more parameters
#surv_val = [100,86.9,74.3,65.3,59.3,55.1,51.7,49.1,46.8,44.5,42.7,40.9,39.4]
#lcw(surv_val,5)

