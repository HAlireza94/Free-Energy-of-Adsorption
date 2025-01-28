# How to setup simulations in LAMMPS?  
all we need to do is to calculate the free energy using thermodynamic integration. We have to do it  
in the following parts:  
* metalic surface + adsorbate + water  
* metalic surface + water  

In the first step, we calculate the free energy using thermodynamic integration which goes over Coulom  
and Lennard-Jones potentials, while in the second one we just do thermodynamic integration on Coulom  
potentials.

