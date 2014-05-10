import sys, os
import numpy as np
import diskLogFast

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

# query = { 'cins':'ING', 'kosId': {'$lt':90000} }
query = 'kosCins=ARA'
aggWons = []
tryValues=[0.5, 2.0]
for i in extramultweights.keys():
    for tryval in tryValues:
        e=dict()
        e[i] = tryval

        r = diskLogFast.doExperiment(query, extramultweights=e, odul = odul, kosCins='ING')
        print i, tryval, r
        aggWons.append( r )
