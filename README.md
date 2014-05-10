anneal<> uses annealing to minimize the function for -won3/tot ratio
fminGeneral<> uses general minimization techniques for the same purpose
	OptimMetods=[ 'Nelder-Mead', 
		     'Powell', 'CG', 'BFGS', 
		     'Newton-CG', 'Anneal', 
		     'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'dogleg', 'trust-ncg']

gminLBGGSB is an application of that. 
fminDiskLogFast2.py uses plain fmin() function Nelder-Mead

diskLogFast and mongoLogFast to retrieve Siralama and Tahminler from txt files.

The exploratary files checked into github