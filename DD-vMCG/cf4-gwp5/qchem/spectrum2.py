# spectrum.py: prints the spectrum energies (x-axis) and intensities (y-axis)
# Usage: python spectrum.py <option=ADC,SRC> <file name>

from myfunctions import *
import sys

fwhm=.5					        # 0.5 eV FWHM for Lorentzian broadening
#weight=float(sys.argv[3])       # weighting coeff

S=[]
for i in range(3,54,2):
   for j in range (1,6):
      pre = "ddtraj" + str(j) + "t" + str(i)
      outfile = pre + ".out"
      xyzfile = pre + ".xyz"
      print outfile
      XAS = read_adc(outfile)
      weight=1
      x,spect = generate_spectrum(XAS,fwhm,weight)	# generate spectrum
      S = S + spect

   # Write spectrum to file
   fname="spectrum" + str(i) + ".dat"
   with open(fname,'w') as f:
      for i in range(len(x)):
         f.write(str(x[i]) + '  ' + str(S[i]) + '\n')
   
