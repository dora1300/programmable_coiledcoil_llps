Programmable Coiled-coil LLPS
==============================
Custom analysis code and MD parameter files related to manuscript "Programmable de novo designed coiled coil-mediated phase separation in mammalian cells". The code in this repository are under the MIT License.

## Description of provided files

### Custom\_scripts
This folder contains the scripts to do the multimerization counting analysis which was used in Figure S5. Molecular dynamics trajectories and an associated topology file (`.pdb` or the like) are provided to `multimerization_analysis.py` which produces a *contact map* of all coil segments in multimers in all analyzed frames, and `contact_analysis.py` determines statistics about those multimers from the contact map, such as multimer lifetimes and the percentage of time that each individual coil is engaged in a multimer interaction, to name a few. These scripts were written specifically for analysis of simulation trajectories for this paper.

Generating data for density profiles, molecular cluster analyses, and mean squared displacement was accomplished using tools provided by GROMACS, e.g. `gmx_density`, `gmx_cluster`, and `gmx_msd` respectively. See GROMACS documentation for how to use these analysis tools. 

### MD\_parameter\_files
This folder contains the `.mdp` files for the single molecule and slab simulation procedures (at both 20 us and 40 us).

### MSD\_analysis
This folder contains the data files and the custom python script to analysis the MSD data to generate effective diffusion coefficients for the proteins. `.csv` files contain average MSD (averaged over all proteins in the slab simulation) for three replicates for the given protein at the listed temperature. Column 1 is the lag-time (tau, ps) and columns 2-4 are the average MSD for all three replicates. `MSD_bootstrap_analysis.py` has the analysis files hardcoded and should only need to be run, with no modification, to generate estimates of effective diffusion coefficients and generate the MSD plot. Keep in mind that because we use bootstrap sampling to estimate diffusion coefficients and error of the estimates, the exact numerical values reported in the paper will not be regenerated.
Internal codenames are used in the file names: 'mcp1' is the simulation of {(gs-S1h-gs-S3h)3 + (gs-S2h)3(gs-S4h)3}; and 'mcp6' is the simulation of {(gs-P5f-gs-P13f)3 + (gs-P6f)3(gs-P14f)3}.

### ProteinBuilding
This folder contains scripts to do protein building, but *only for* proteins with parallel and antiparallel coil segments. Instructions and an example are provided. 

Instructions for making proteins that do not specify orientation (anything that is *not* APPAP, APPAPAPPAP, or PPPPPPAAAA) can be found in a repository for a related paper. The repository is [linked here](https://github.com/dora1300/cc_llps_framework).

As described in the paper, once a protein is made, you can then run single molecule simulations on it using the appropriate `.mdp` files (described above) and then pack configurations of a desired density into a box of desired size using `Packmol v. 20.3.2`.

### Topologies
This folder contains all of the topology files (`.itp` and `.top`) for all of the proteins described in this manuscript. Each protein pair is given its own folder. `.top` files are predesigned for slab simulations.

#### Additional\_combinations
This folder contains topology (`.itp` and `.top`) files for the additional combinations of mixtures of peptides from Supplementary Figure 15.


## Guidelines for reproducing data
Due to the large size of individual simulation trajectories (&#076; 3 Gb), trajectories are not provided. You can follow these guidelines to reproduce trajectory data.
1. Write a protein `design_file.csv` (see README in the `ProteinBuilding` directory) for whichever protein you want
2. Run a single molecule simulation at the desired slab temperature using the provided `.mdp` files. 
    - takes less than 1 hour using 1 thread on a Mac with a 2 Quad-core CPU
3. Randomly select 5 configurations from the equilibrated portion of the single molecule simulation (using whatever random selection method you'd like)
4. Pack enough copies of all 5 configurations to reach the desired coil segment density in the box
5. Run the slab protocol (EM--NPT--NVT--Production MD steps) using the provided `.mdp` files.
    - EM--NPT--NVT steps take less than 8 hours on a high performance computer using 4 processes
    - the slab production step takes, on average, less than 7 days on a high performance computer using 24 processes
6. Use `gmx_density` to determine the equilibrated portion of the trajectory, then to do profile analysis, and `gmx_clustsize` to calculate cluster size information
7. Feed the trajectory into `multimer_analysis.py` to quantify the different multimers in the *equilibrated portion* of the trajectory, and then take the contact map data from the multimer analysis and feed into `contact_analysis.py` to determine the percentage of simulation time that individual coils are engaged in a multimer.


## Software requirements and details

### Molecular simulation software
We used GROMACS v2022.1 to run all molecular dynamics simulations, both single molecule and slab, for this study. The specific details of compilation and types of computers used are described in the manuscript both in Methods and Supplemental Methods. 

You may download GROMACS v2022.1 [at this link](https://manual.gromacs.org/2022.1/download.html), and you can reference the documentation for this specific version [at this link](https://manual.gromacs.org/2022.1/index.html). GROMACS compilation is hardware specific and so we cannot provide precompiled binaries of GROMACS. Installation is quick (within 2 hours) and is easy to do following the instructions provided in the documentation.

We used following compilers were used to compile GROMACS:
- MacOS (Clang 12.0.0)
- Ubuntu (GCC 11.3.0)
- RHEL (GCC 11.2.0; OpenMPI 4.1.1)


### Requirements to run custom scripts
Custom scripts -- which include the custom analysis scripts (see `Custom_scripts`, above) and the scripts used to make proteins (see `ProteinBuilding`, above) -- use python v3.9. Other versions of python have not been tested. The following dependencies are also needed:
- matplotlib (3.7.1)
- numpy (1.21.5)
- mdtraj (1.9.7)
- ProDy (2.3.1)
- PeptideBuilder (1.1.0)
- Biopython (1.80)
- pandas (1.4.4)
- scipy (1.9.1)

These scripts were run on the following operating systems:
- MacOS 12.6.3
- Ubuntu 22.04.2 LTS
- RHEL 7.9 (codename Maipo)


### Installation guide
Running the custom scripts requires installing the above listed dependencies (and their own subsequent dependencies). Installing GROMACS requires following the instructions provided in its documentation (see link above). GROMACS installation is the limiting step, and should take less than 2 hours on a normal computer. If you have access to a high performance computer, GROMACS might already be installed.


## Copyright

Copyright (c) 2023, Ramirez et al.
