#!/bin/bash
# Generate $1 ddtraj files (up to total number of GWPs)

for i in $(seq 1 $1)
do
	./gentraj.expect $i
	sleep 1
	mv ddtraj.pl ddtraj$i.pl
done
