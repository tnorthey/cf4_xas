#!/bin/bash
# Creates QChem input file from xyz file $1
# based on template-adc.inp1 and template-adc.inp2

for i in *.xyz
do

cat template-adc.inp1 > ${i%.*}.inp
tail -n +3 $i >> ${i%.*}.inp
cat template-adc.inp2 >> ${i%.*}.inp

done

