# How to run the scripts?


Step 1: Download and install DDEC from https://sourceforge.net/projects/ddec/files/  
Step 2: Create a directory in which there are POTCAR, CHGCAR, AECCAR0, AECCAR2 files obtained from DFT, let's name this directory as "Charge".  
Step 3: Copy the executable bash that is DDEC generated from Fortran to the Charge directory.  
Step 4: Place "job_control.txt" in Charge directory.  
Step 5: Execute the bash, it will take a few minutes or so.  
Step 6: DDEC6_even_tempered_net_atomic_charges.xyz is the file we want because it has not only partial charges calculated by DDEC but also cartesian coordinates.  
