import sys, os
import numpy as np
import scipy as sp
import scipy.optimize as optimize
import diskLogFast

query = { 'cins':'ING', 'kosId': {'$lt':90000} }
odul = [1.75, 1.25, 1.01]
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

def f(ev):
   e = extramultweights
   for n,i in enumerate(e.keys()): e[i]=ev[n]
   r = diskLogFast.doExperiment(query, extramultweights=e, kosCins='ARA')
   print "INPUT", e
   print "AGG PERCENTAGES W1 W2 w3 W4: ", r
   return -r[2]

#
x=optimize.fmin(f, extramultweights.values(), disp=True)
print x


