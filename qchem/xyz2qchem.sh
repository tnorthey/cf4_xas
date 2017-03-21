#!/bin/bash
# Creates QChem input file from xyz file $1
# based on template-adc.inp1 and template-adc.inp2

cat template-adc.inp1 > ${1%.*}.inp
tail -n +3 $1 >> ${1%.*}.inp
cat template-adc.inp2 >> ${1%.*}.inp

