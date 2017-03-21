# spectrum.py: prints the spectrum energies (x-axis) and intensities (y-axis)
# Usage: python spectrum.py <option=ADC,SRC> <file name>

from myfunctions import *
import sys

option=sys.argv[1].lower()	# adc/src option, case insenstive 
filename=sys.argv[2]		# file name

if option=='adc':
   XAS = read_adc(filename)
elif option=='src':
   XAS = read_src(filename)
else: 
   print "Error: Pick option='ADC' or 'SRC'"

fwhm=.5					# 0.5 eV FWHM for Lorentzian broadening 
x,spect = generate_spectrum(XAS,fwhm)	# generate spectrum

# Write spectrum to file
with open('spectrum.dat','w') as f:
   for i in range(len(x)):
      f.write(str(x[i]) + '  ' + str(spect[i]) + '\n')

