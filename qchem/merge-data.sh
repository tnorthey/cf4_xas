#!/bin/bash

for i in ddtraj*.dat
do
	awk '{print $2}' $i > ${i%.*}.column2
done

paste -d' ' *.column2 > data3d.dat
rm *.column2

