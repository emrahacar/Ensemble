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

def f(evAndodul):
   e = extramultweights
   for n,i in enumerate(e.keys()): e[i]=evAndodul[n]
   odul=evAndodul[-4:]
   r = diskLogFast.doExperiment(query, extramultweights=e, odul=odul, kosCins='ARA')
   print "INPUT MIX:", e
   print "INPUT ODUL:", odul
   print "AGG PERCENTAGES W1 W2 w3 W4: ", r
   return -r[2]

#

e = extramultweights
bounds=[]
initx=[]
# bounds for mult-weights
for e in e.keys():
   bounds.append( (0.0,2.0) )
   initx.append(1.0)
# bonds for odul
for i in range(4): bounds.append( (0.0, None) )
initx = initx + [1.75, 1.25, 1.01 , 0.0 ]
x=optimize.fmin_l_bfgs_b(f, initx, approx_grad=True, bounds=bounds, iprint=1, epsilon=1e-3, disp=True)
print x


