# cf4_xas

## Usage

#### Direct dynamics

Create an input file and folder for a new run,

	cp example.inp run1.inp
	cp -r example/ run1/

then edit run1.inp, selecting the title of the run ('name' parameter) number of GWPs (ngwp), the direct-dynamics method (e.g. title = UHF/6-31G\*), the total time in fs (tfinal), and specify the stationary point geometry (INITIAL-GEOMETRY-SECTION) and energy (ener0). It should look like,

	#######################################################################         
	###              DD / Propagation in normal modes                  ####
	#######################################################################         
	
	RUN-SECTION                                                                     
	name = example   ngwp = 1
	direct = cartesian 
	title =  UHF/6-31g*. 
	propagation
	tfinal = 200.0   tout = 1.0   tpsi= 1.0                       
	psi  gridpop   update  steps auto
	end-run-section                                                                 
	
	INITIAL-GEOMETRY-SECTION
	cartesian = angst
	  6    -0.69934   2.34967   0.00000 
	  9     0.60215   2.34967  -0.00000 
	  9    -1.13316   3.29245   0.78541 
	  9    -1.13317   1.19810   0.42375 
	  9    -1.13317   2.55847  -1.20916 
	end-cartesian
	end-initial-geometry-section
	                         
	INTEGRATOR-SECTION       
	VMF
	rk5/all = 1d-5,minstep 1.0d-4
	default
	gwp_eoms=tikhonov
	#gwp_model=classical
	end-integrator-section
	
	DIRDYN-SECTION
	data = dd_data
	update = always
	qcprogram = gaussian     method = uhf 
	ener0 = -435.067762856
	dd_adiab
	db = rdwr
	subcmd = g09
	ascii_db
	dbsave
	end-dirdyn-section
	
	end-input
	

Check the other setup files in the dd\_data/ folder, the refdb.dat file should look like,

	     10.100200001000
	# Natm, Nstate
	        5    1
	# E0
	   -435.067762856
	# Symmetry nos.
	      3      3
	# Mass 
	  21874.661799000001  34902.226103181638  34902.226103181638  34902.226103181638
	  34902.226103181638
	# Name, Xcoo
	  6    -0.69934   2.34967   0.00000
	  9     0.60215   2.34967  -0.00000
	  9    -1.13316   3.29245   0.78541
	  9    -1.13317   1.19810   0.42375
	  9    -1.13317   2.55847  -1.20916	

Make sure each parameter is correct, such as Natm, Nstate, E0 (should match ener0 in run1.inp), and the 'Mass' and 'Name, Xcoo' sections. Finally, check the template.dat file which should look like,

	%mem=5000MB
	%Nprocshared=6
	%chk=$chk0$
	#P UHF/6-31g* IOP(7/33=1) IOP(7/8=11) 
	$Freq:Freq$
	
	CF4+
	
	1 2
	<geometry>
	
	
Make sure the method is correct (in this case UHF/6-31G\*), change the number of processors (%Nprocshared) to use as needed, and check that the charge and spin mutiplicity (CF4+ has +1 charge and is a doublet, 2S+1=2).

Now start the new run,

	quantics -w run1.inp

This generates files in the run1 folder and some other checkpoint files. Once complete, the "output" file contains the gross Gaussian populations and other information. The nuclear coordinates can be printed to a nice format with 'ddtraj', the script gentraj.sh does this for N GWPs (in our example there is 1),

	./gentraj.sh 1

This outputs ddtraj1.pl, ddtraj2.pl, ... for each GWP. These contain the time-evolving nuclear coordinates.

The example run only propagates 1 GWP for 200 fs.

#### XAS

To compute the XAS, the CVS-ADC(2) method in QChem will be used.

Edit the variables.py file which looks like,

	runfolder = 'example' 	    # run folder
	fname = 'example/output'    # path of quantics 'output' file
	Nat = 5                     # Number of atoms
	Nstate = 1                  # Number of states
	Ngwp = 1                    # Number of GWPs
	Nt = 51                     # Number of time-steps

The runfolder and the path of the output file would be 'run1' and 'run1/output' in this case. Make sure the Nat, Nstate, Ngwp are correct. Nt is the number of time-steps to generate xyz files for (which will then be used to generate spectra), it can be less than the total time-steps used in the dynamics. To generate the xyz files to the qchem folder,

	python traj2xyz.py

To create the QChem input files, first check the qchem/template-adc.inp1 file:

	$comment
	XAS calculation for valence excited states for CF4+ using cvs-adc(2) + 6-31G* basis set
	job 1 - determination of HF orbitals
	$end
	
	$molecule
	1 2

Be sure the charge and spin multiplicity are correct. Then, check the qchem/template-adc.inp2 file:

	$end
	
	$comment
	cvs-adc(2) calculation
	$end
	
	$rem
	mem_total 3000
	mem_static 1500
	sym_ignore true
	method cvs-adc(2)-x
	basis 6-31G*
	ee_singlets 20
	cc_rest_occ 5                  !only excitations from the lowest N orbitals
	unrestricted  true
	max_scf_cycles 200
	SCF_CONVERGENCE = 6
	$end
	
Choose the method (e.g. CVS-ADC(1), CVS-ADC(2), CVS-ADC(2)-x) and basis set appropriately. Finally, create the input files with,

	cd qchem/
	for i in *xyz
	do
	./xyz2qchem $i
	done

This creates Nt\*Ngwp .inp files. They can be run as needed (e.g. paste the following into a bash script),

	for i in *.inp
	do
	qchem $i ${i%.*}.out	
	done
	
Generate spectra with the spectrum.py function, 

	python spectrum.py adc qchem/qchem.out 1.0
	
A file 'spectrum.dat' will be generated. The 'adc' option is needed here, for the QChem output file 'qchem/qchem.out', and the spectrum will be weighted by a factor of 1.0 in this case. Ideally, use the Gaussian weighting coefficients in the quantics 'output' file.



