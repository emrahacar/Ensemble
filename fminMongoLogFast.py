import sys, os
import numpy as np
import scipy as sp
import scipy.optimize as optimize
import mongoLogFast

query = { 'cins':'ING', 'kosId': {'$lt':90000} }
odul = [1.75, 1.25, 1.01]
# odul = [2, 1.5, 1, 0.5]
extramultweights = { 'lgbmS' : 1.0, 
                     'lrfSTbl' : 1.0,
                     'lgbmHiz' : 1.0, 
                     'lgbmHizTbl' : 1.0,
                     'lHC': 1.0,
                     'ladaS': 1.0,
                     'lrfS': 1.0,
                     'lgbmS3Tbl': 1.0,
                     'l': 1.0,
                     'lDerece': 1.0,
                     'ladaSTbl': 1.0,
                     'lpoisg': 1.0,
                     'lDereceTbl': 1.0,
                     'lg': 1.0,
                     'lTbl': 1.0,
                     'lpoisgTbl': 1.0,
                     'lgTbl': 1.0 } 

def f(o):
   r = mongoLogFast.doExperiment(query, odul = o)
   return r[2]

x=optimize.fmin(f, odul, maxiter=20, disp=True)
print x


