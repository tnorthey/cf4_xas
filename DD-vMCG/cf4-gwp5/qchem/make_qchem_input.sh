#!/bin/bash

cat template-adc.inp1 > ${1%.*}.inp
tail -n +3 $1 >> ${1%.*}.inp
cat template-adc.inp2 >> ${1%.*}.inp

