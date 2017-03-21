def read_xyz(fname):
   ##################################################
   # read_xyz:	Reads xyz file 'fname'
   # Inputs:	fname, the file name of the xyz file to read
   # Outputs: 	AtomList (string list), list of atomic labels; 
   # 		Coords (float list), coordinates as column vector with the format X1,Y1,Z1,X2,Y2,Z2,...
   ##################################################
   with open(fname,'r') as f:			# open file   
      AtomList=[]; Coords=[]
      c=0
      f.next()					# Skip line
      for line in f:
         c+=1				
         if c==1:
            comment = line
	 else:
            AtomList.append(line.split()[0]) 	# List of atomic labels
            for i in range(1,4):
               Coords.append(float(line.split()[i]))
   ##################################################dd
   return AtomList,Coords,comment


def write_xyz(AtomList,Coords,fname,comment):
   ##################################################
   # write_xyz: Write xyz file 'fname' using atom list 'AtomList' and Cartesian coordinates 'Coords'
   # Inputs:	AtomList (string list), list of atomic labels
   # 		Coords (float list), coordinates as column vector with the format X1,Y1,Z1,X2,Y2,Z2,... 
   # 		fname (str), output xyz file name  
   #		comment (str), comment line in the xyz file
   # Outputs:	'fname' (file), xyz file
   ##################################################
   Nat=len(AtomList)					# Number of atoms
   with open(fname,'w') as f:				# Open file for writing
      f.write(str(Nat)+'\n')				# The first line of an xyz file contains only the number of atoms
      f.write(comment + '\n')				# The second line is blank or contains a title string (convention)
      for i in range(3*Nat):				# Loop over vectors of lentgh 3*Nat
         if i%3==0:					# Indices 0,3,6,...
            Atom=AtomList[i/3]				# Read atom labels (at indices 0,1,2,... every i=0,3,6,...)
            x = Coords[i]				# x coordinate
         elif (i-1)%3==0:				# Indices 1,4,7,...
            y = Coords[i]				# y coordinate
         elif (i-2)%3==0:				# Indices 2,5,8,...
            z = Coords[i]				# z coordinate
            f.write( Atom + '  ' + str(x) + '  ' + str(y) + '  ' + str(z) + '\n')	# Write out Lines containing atom labels and x,y,z coordinates
   ################################################## 
   return


def read_displacements(Nat,imode):
   ##################################################
   # read_displacements: Reads displacement coordinates for mode 'imode' from 'normalmodes.txt'
   # Inputs: 	Nat (int), total number of atoms
   #		imode (int), the displacements are taken from mode number 'imode'
   # Outputs:	D (float list), single column of displacement coordinates (length 3*Nat)
   ##################################################
   # Definitions
   N = 3*Nat  # Number of coordinates
   # Error checks
   if Nat==2:
      Nmode=2
   elif Nat>2:
      Nmode=N-6
   else:
      print "ERROR: Something wrong with number of atoms"
      print "Are there <2 atoms?"
      return
   
   if imode>=1 and imode<=Nmode:
      print "Reading displacements for mode " + str(imode)
   else:
      print 'ERROR: imode out of range (1,Nmode).'
      return
   # Known pattern of g09 frequencies output file...
   row = int((imode-1)/5)
   a = (row+1)*7 + row*N
   b = (row+1)*(7 + N)
   d = row*5
   # Append displacements from file to column vector 'Displc'
   c=0
   Displc=[]
   with open('inputs/normalmodes.txt','r') as f:
      for line in f:
         c+=1
         if c>a and c<=b:
            Displc.append(float(line.split()[imode+2-d]))
   ##################################################
   return Displc


def read_gwpcentres(Nstate,istate):
   ##################################################
   # read_gwpcentres: Read displacement factors from file 'gwpcentres' for state 'istate'.
   # Inputs: 	Nstate (int), the total number of states
   #		istate (int), the state to read
   # Outputs:	Time (float list), list of time in atomic units 
   # 		v (float array), displacement factors array with columns 0,1,...,Nmode-1 pertaining to modes 1,2,...,Nmode, rows correspond to Ng Gaussians
   ##################################################
   Time=[]; v=[]; c=0; x=0
   with open('inputs/gwpcentres','r') as f:
      for line in f:
         c+=1
         if c==1:					# Line 1 contains Nmode and Ng
            Nmode=int(line.split()[1])			# Number of modes
   	    for i in range(Nmode):
               v.append([])
	    Ng=int(line.split()[2])			# Number of Gaussians
   	    rep=Nstate*(Ng+1)+1				# gwpcentres repeats every Nstate*(Ng+1)+1 lines
            print "There are Nmode = " + str(Nmode) + " modes in gwpcentres"
            print "There are Ng = " + str(Ng) + " Gaussians in gwpcentres"

         elif c>1:					# Lines >1 have time and displacement factors
            if (c-2)%rep==0:				# Repetition every 'rep' lines
               #print "t lines: " + line
               Time.append(float(line.split()[1]))	# List of time in atomic units
            elif (c-x-4-(istate-1)*(Ng+1))%rep==0:	# This fits the formatting of the gwpcentres file
               #print "v lines: " + line
	       for imode in range(Nmode):
	          v[imode-1].append(float(line.split()[imode-1]))
	       x+=1					# counter causes Ng lines to be appended (which is what we want)
	       if x==Ng:				# stop appending after Ng lines
		  x=0					# reset counter 
   # Checks
   Nt = len(Time)
   print "There are Nt = " + str(Nt) + " total time-steps"
   print "Displacement factor array has " + str(len(v[0])) + " rows"
   if len(v[0])==Nt*Ng:
      print "There are Nt*Ng = " + str(Nt*Ng) + " rows of displacement factors, as there should be."
   else:
      print "Error: There are " + str(Nt*Ng) +  " =/= Nt*Ng rows of displacement factors! Exiting..."
      return
   ##################################################
   return Nmode,Ng,Time,v 


def read_output(Nstate,Ng):
   ##################################################
   # read_output: Read Gaussian weights (and state weights) from file 'output' for state 'istate'.
   # Inputs: 	Nstate (int), total number of states
   # 	 	Ng (int), total number of Gaussians
   # Outputs:	Time (float list), list of time in fs 
   # 		gWeights (float array), Gaussian populations with columns 0,1,...,Ng-1 pertaining to Gaussians 1,2,...,Ng
   ##################################################
   Time=[]; gWeights=[]
   X=0; c=0; j=0
   for i in range(Ng):
      gWeights.append([])
   with open('inputs/output','r') as f:
      for line in f:
         if line[1:5]=='Time':
            Time.append(float(line.split()[2]))
	 elif line[1:len('Gross Gaussian Populations')+1]=='Gross Gaussian Populations':
            istate = int(line.split()[7])			# state number = 1,2,...
            X=(Ng-1)/7+1					# Causes the next X lines to be read in the following elif block
	 elif X>0:
	    c+=1						# Line counter for Gaussian populations part
	    for i in range(7):
	       j+=1
	       gWeights[i+7*(c-1)].append(float(line.split()[3+i]))
	       if j==Ng:					# break after Ng floats have been appended to gWeights
	          break
            if c==X:
               X=0; c=0; j=0					# reset counters
	       # print "X reset to 0"	
	 #else:	
	 #   print "Line not read."
   # Checks
   ##################################################
   return Time,gWeights


def read_adc(ADCoutput):
   ##################################################
   # read_adc: Reads excitation energies and oscillator strengths from qchem XAS ADC calculation output.
   # Inputs:    ADCoutput (str), ADC output file name
   # Outputs:   XAS (float array), XAS[0] = energies, XAS[1] = oscillator strengths 
   ##################################################
   XAS=[];
   XAS.append([])
   XAS.append([])
   c=0
   str1='Excitation energy:'
   str2='Osc. strength:'
   with open(ADCoutput,'r') as f:
      for line in f:
         if line[2:len(str1)+2]==str1:
            if c==0:
	       #print line.split()[2]
               E=float(line.split()[2])
	       c=1
	 elif line[2:len(str2)+2]==str2:
	    if c==1:
	       #print line.split()[2]
	       XAS[1].append(float(line.split()[2]))
	       XAS[0].append(E)
	       c=0
            
   # Checks
   ##################################################
   return XAS


def read_src(SRCoutput):
   ##################################################
   # read_src: Reads excitation energies and oscillator strengths from qchem XAS SRC calculation output.
   # Inputs:    SRCoutput (str), SRC output file name
   # Outputs:   XAS (float array), XAS[0] = energies, XAS[1] = oscillator strengths 
   ##################################################
   XAS=[];
   XAS.append([])
   XAS.append([])
   c=0
   str1='Excited state'
   str2='Strength'
   with open(SRCoutput,'r') as f:
      for line in f:
         if line[1:len(str1)+1]==str1:
            if c==0:
               #print line.split()[2]
               E=float(line.split()[7])
               c=1
         elif line[4:len(str2)+4]==str2:
            if c==1:
               #print line.split()[2]
               XAS[1].append(float(line.split()[2]))
               XAS[0].append(E)
               c=0

   # Checks
   ##################################################
   return XAS


def generate_spectrum(XAS,fwhm):
   ##################################################
   # generate_spectrum: Generates spectrum with Lorentzian broadened lines (with FWHM=0.5 eV) 
   # Inputs:    XAS (float array), XAS[0] = energies (eV), XAS[1] = oscillator strengths
   # 		fwhm (float), full-width half-maximum for Lorentzian broadening (eV) e.g. 0.5 eV
   # Outputs:   x (float list), x-axis energies (eV)
   # 		spect (float list), spectrum (arb. units) with Lorentzian broadened lines 
   ##################################################
   E=XAS[0]			# Line energies
   Emin=int(E[0]-1.5)		# Min energy
   Emax=int(E[-1]+1.5)		# Max energy
   A=XAS[1]			# Line intensities
   x=[]
   res=300			# Number of spaces along x-axis (arbitrary)
   x=linspace(Emin,Emax,res)
   
   spect=[]
   for i in range(len(x)):
      spect.append(float(0.))	# define spectrum blank list
  
   g=(fwhm/2.)**2		# Factor in Lorentzian function
   for j in range(len(A)):
      a=A[j]			# amplitude of line j
      e=E[j]			# energy of line j
      for i in range(len(x)):
         
         Lorentz = a*g/( (x[i]-e)**2 + g )		# Lorentzian broadening
         spect[i]=spect[i]+Lorentz			# XAS

   return x,spect


def displace_coords(Coords,imode,Factor):
   ##################################################
   # displace_coords: Displace coords from xyz file 'xyzfile' along mode 'imode' (0<int<=Nmode) by 'Factor' (float)
   # Inputs:	Coords (float list), coordinates as column vector with the format X1,Y1,Z1,X2,Y2,Z2,...
   #		imode (int), the coordinates are displaced along mode number 'imode'
   # 		Factor (float), the coordinates are displaced along mode number 'imode' by 'Factor' atomic units  
   # Outputs:	D (float list), displaced coordinates with same formatting as 'Coords'
   ##################################################
   Nat=len(Coords)/3				# Number of atoms 
   Displc=read_displacements(Nat,imode)		# Read normal mode displacements (vector of length 3*Nat)
   D=[]
   for i in range(3*Nat):			# Loop over coordinates
      D.append(Coords[i] + Factor*Displc[i]) 	# Displaced coordinates
   ################################################## 
   return D


def linspace(a, b, n=100):
    # Matlab-like linspace function
    if n < 2:
        return b
    diff = (float(b) - a)/(n - 1)
    return [diff * i + a  for i in range(n)]


def generator_(tstep,istate,Nstate,Modes,xyzfile):
   ##################################################
   # generator_: Generates xyz files (with the spectral weighting in the comment line) for all Gaussians for time-step 'tstep' and state 'istate'   
   # Inputs:    tstep (int), time-step number (0,1,2,...)
   #            istate (int), electronic state (1,2,...)
   # 		Nstate (int), total number of states
   # 		Modes (int array), normal mode numbers e.g. [11,3,14,8]
   # 		xyzfile (str), path of xyz file containing initial coordinates (usually the equilibrium geometry)
   ##################################################

   AtomList,R0,comment = read_xyz(xyzfile)
   Nmode,Ng,Timeau,v = read_gwpcentres(Nstate,istate)
   Timefs,gWeights = read_output(Nstate,Ng)   # Read time-steps (fs), and Gaussian weights      
   au2ang = 0.52918
   
   print 'generator_: Generating xyz files for t = ' + str(Timefs[tstep]) + ' (fs)'
   
   ####################################################
   
   for j in range(Ng):			# Loop over Gaussians
      D=R0						# Starting coordinates
      # gWeights[column][row] = gWeights[Gaussian index][time-step 1: state 1, state 2, ...; time-step 2: state 1, state 2, ...; ...]
      A = gWeights[j][istate-1+Nstate*tstep]     
      for i in range(len(Modes)):			# Loop over modes
         imode=Modes[i]				# Mode number
         # v[column][row] = v[mode index][Gaussian index]
         Factor = v[i][Ng*tstep+j]*au2ang	# Displacement factor in atomic units of length (then converted to Angstrom)
         # print Factor
         D = displace_coords(D,imode,Factor)	# Displace coordinates along mode 'imode' by 'Factor'
      if A>1e-2:				# Only write xyz file if weighting coeff. is non-negligible 
         fname='state' + str(istate) + 'tstep' + str(tstep) + 'g' + str(j)  + '.xyz'	# Output file name
         comment=str(A)
         write_xyz(AtomList,D,fname,comment)	# write to xyz
   ####################################################
   return


