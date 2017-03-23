#!/bin/bash

for i in qchem/*out
do
	python spectrum.py adc $i 1.0 290 320
	mv spectrum.dat ${i%.*}.dat
done

