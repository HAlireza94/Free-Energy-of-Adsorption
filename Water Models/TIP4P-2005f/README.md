## This is a test for TIP4P/2005f done in GROMACS 2020.7  
After finishing the simulation, make an index.ndx file using gmx make_ndx -f conf.gro, then open the index.ndx and at the bottom add [mol], then in the next line add 1 2 3 4. This is the index of O, H, H, M for the first molecule. Now, do the gmx trjconv -f MD.xtc -s MD.tpr -n index.ndx -pbc mol -b 0 -o checking.gro . In the prompt, use the group number corresponding to "mol" that we created in the index file. After that you can get the average bond length between H and O, average teta between H - O - H, and average distance between M and O. Note, M stands for dummy atom in this 4 point water model.  

The output using ANAL.py for averaging over 1001 frames as below:  
1001 frames have been processed  
<teta> = 107.4163  
<r_OH> = 0.9419  A  
<d_OM> = 0.1472  A  
