#!/usr/bin/gnuplot
#
# Interpolating a heat map
#
# AUTHOR: Hagen Wierstorf
# VERSION: gnuplot 4.6 patchlevel 0

reset

# wxt
set terminal wxt size 1200,800 enhanced font 'Verdana,10' persist
# png
#set terminal pngcairo size 350,262 enhanced font 'Verdana,10'
#set output 'heat_map_interpolation3.png'

set title "CF4+ XAS during dissociation"
set xlabel "t (fs)"
set ylabel "E (eV)"
set xrange [0 : 50]
show xrange
set yrange [0 : 300 ]
show yrange
set ytics ("290" 0,"295" 50,"300" 100,"305" 150,"310" 200,"315" 250,"320" 300)

set border linewidth 0
unset key
#unset colorbox
#unset tics
#set lmargin screen 0.1
#set rmargin screen 0.9
#set tmargin screen 0.9
#set bmargin screen 0.1
#set palette grey

set pm3d map
set pm3d interpolate 0,0
splot 'combined.dat' matrix

set output "data3d.png"
set term pngcairo size 1200,800
replot
set term x11


