from myfunctions import *

fname='output'
Nstate=1
Ng=5

Time,gWeights=read_output(fname,Nstate,Ng)

Ngwp=5
Nat=5       
Nt=55      # number of time-steps

for x in range(1, Ngwp + 1):
   ddtraj="ddtraj" + str(x) + ".pl"
   AtomList,Coords=read_ddtraj(ddtraj)
   c=0
   d=0
   alist=[]
   clist=[]
   for i in range(0, 3*Nt*Nat):
      c+=1
      clist.append(Coords[i])          # coordinates
      if c%3==0:
         alist.append(AtomList[i/3])   # Atomic numbers
      if c%(Nat*3)==0:
          fname="ddtraj" + str(x) + "t" + str(d) + ".xyz"
          comment=str(gWeights[x-1][d])
          write_xyz(alist,clist,fname,comment)
          c=0
          d+=1
          alist=[]
          clist=[]

print str(Ngwp*Nt) + " xyz files generated!"

