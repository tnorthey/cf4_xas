#!/bin/bash
# Generate ddtraj files for each GWP
# must edit {1..N} where N is the number of GWPs
for i in {1..5}
do
	./gentraj.expect $i
	sleep 1
	mv ddtraj.pl ddtraj$i.pl
done
