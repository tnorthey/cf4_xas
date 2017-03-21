
set terminal png size 1600,1200 enhanced font "Helvetica,24"
set output 'output.png'
set title "CF4+ XAS, Carbon edge"
set xlabel "E (eV)"
set ylabel "Intensity (arb. units)"
#set xrange [408:416]

plot "cvs-adc1.dat" using 1:2 title 'CVS-ADC(1)' with lines, \
     "cvs-adc2s.dat" using 1:2 title 'CVS-ADC(2)-s' with lines, \
     "cvs-adc2x.dat" using 1:2 title 'CVS-ADC(2)-x' with lines

