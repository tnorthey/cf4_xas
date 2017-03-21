from myfunctions import *

fname='output'
Nstate=1
Ng=5

Time,gWeights=read_output(fname,Nstate,Ng)

print gWeights

