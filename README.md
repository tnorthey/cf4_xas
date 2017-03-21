# cf4_xas

## Usage

Create an input file and folder for a new run,

	cp example.inp run1.inp
	cp -r example/ run1/

then edit run1.inp, selecting the number of GWPs, the direct-dynamics method (e.g. UHF/6-31G\*), and specify the stationary point energy. It should look like,

	#######################################################################         
	###              DD / Propagation in normal modes                  ####
	#######################################################################         
	
	RUN-SECTION                                                                     
	name = example   ngwp = 1
	direct = cartesian 
	title =  UHF/6-31g*. 
	propagation
	tfinal = 10.0   tout = 1.0   tpsi= 1.0                       
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

Make sure each parameter is correct, such as the Natm, Nstate, E0, and the Mass and Name Xcoo sections. Next check the template.dat file which should look like,

	%mem=5000MB
	%Nprocshared=6
	%chk=$chk0$
	#P UHF/6-31g* IOP(7/33=1) IOP(7/8=11) 
	$Freq:Freq$
	
	CF4+
	
	1 2
	<geometry>
	
	
Make sure the method is correct (in this case UHF/6-31G\*), change the number of processors to use as needed, and check that the charge and spin mutiplicity is right (CF4+ has +1 charge and is a doublet, 2S+1=2).
Now start the new run,

	quantics -w run1.inp

This generates an "output" which contains the gross Gaussian populations and other information. The nuclear coordinates can be printed to a nice format with 'ddtraj', the script gentraj.sh does this for N GWPs (in our example there are 5),

	./gentraj.sh 5 

This outputs ddtraj1.pl, ddtraj2.pl, ... for each GWP. These contain the time-evolving nuclear coordinates.
