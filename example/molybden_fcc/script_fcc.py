# script for running lammps simulations for Molybden fcc on Maxwell

import os

# counters
timesteps_together = 0
num = 1
temperature = 600

# I want 36000 timesteps (as in article)
while timesteps_together < 1000:
    
	input_script = """
# Mo, fcc
# # ---------- Initialize Simulation --------------------- 
clear 
units           metal 
dimension       3 
boundary        p p p 
atom_style      atomic 
atom_modify     map array

# # ---------- Create Atoms --------------------- 
lattice         fcc 4.00
region          box block 0 5 0 5 0 5 units lattice
create_box      1 box
create_atoms    1 box

# # ---------- Define Interatomic Potential --------------------- 
pair_style      eam/alloy 
pair_coeff      * * Mo_Zhou04.eam.alloy Mo
neighbor        2.0 bin 
neigh_modify    delay 10 check yes 

#  # ---------- Define Settings --------------------- 
compute         eng all pe/atom
compute         eatoms all reduce sum c_eng 

#  # ---------- Run Minimization --------------------- 
reset_timestep  0 
fix             1 all box/relax iso 0.0 vmax 0.001
thermo          10 
thermo_style    custom step pe lx ly lz press pxx pyy pzz c_eatoms 
min_style       cg 
minimize        1e-25 1e-25 5000 10000 
unfix           1

#  # ----------- Run simulation of fcc phase of Mo --------------------
reset_timestep  0
thermo          10
thermo_style    custom step lx ly lz press pxx pyy pzz pe temp
thermo_modify   format 2 %22.18f
velocity        all create {} 12345 mom yes rot no
dump            1 all custom 50 dumpMoBcc{}.out id type x y z
fix             2 all npt temp {} {} 1 iso 0 0 1 drag 1
run             9999

#-------------------------------------------------
""".format(temperature, num, temperature, temperature)

	print(input_script)
	
	# create input script file
	script_name = "Mo_fcc.in"
	os.system("touch {}".format(script_name))
	
	# erase old code
	open(script_name, "w").close()
	
	# paste new code
	file = open(script_name, "w")
	file.write(input_script)
	file.close()
	
	# run simulation
	os.system("cat {}".format(script_name))
	os.system("mpirun -np 4 lmp -in {}".format(script_name))
	
	# raise counters	
	timesteps_together += 200
	num += 1
	
	
