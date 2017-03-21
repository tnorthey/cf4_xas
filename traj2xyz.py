from myfunctions import *
from variables import *

Time,gWeights=read_output(fname,Nstate,Ngwp)

print "Total time-steps in 'output' file = " + str(len(Time))

for x in range(1, Ngwp + 1):            # loop over GWPs
   ddtraj= str(runfolder) + "/ddtraj" + str(x) + ".pl"     # DD trajectory files
   AtomList,Coords=read_ddtraj(ddtraj)  # read atoms and coordinates
   c=0; d=0; alist=[]; clist=[]         # initialise variables
   for i in range(0, 3*Nt*Nat):         # loop over atomic coordinates and time-steps
      c+=1
      clist.append(Coords[i])           # coordinates
      if c%3==0:
         alist.append(AtomList[i/3])    # Atomic numbers
      if c%(Nat*3)==0:                  
          fname="qchem/ddtraj" + str(x) + "t" + str(d) + ".xyz"         # name of xyz file
          comment=str(gWeights[x-1][d])                                 # comment with the Gaussian weighting coefficient 
          write_xyz(alist,clist,fname,comment)                          # write the xyz file
          c=0
          d+=1
          alist=[]
          clist=[]

print "traj2xyz complete: " + str(Ngwp*Nt) + " xyz files generated!"

