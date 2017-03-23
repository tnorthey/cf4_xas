
set title "CF4+ XAS during dissociation"
set xlabel "E (eV)"
set ylabel "Intensity (arb. units)"

plot "ddtraj1t0.dat" u 1:2 w l t "t = 0 fs" lw 2 
replot "ddtraj1t10.dat" u 1:2 w l t "t = 10 fs" lw 2 
replot "ddtraj1t20.dat" u 1:2 w l t "t = 20 fs" lw 2 
replot "ddtraj1t30.dat" u 1:2 w l t "t = 30 fs" lw 2 

set output "data.png"
set term pngcairo size 1200,800
replot
set term x11

