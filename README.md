Programmable Coiled-coil LLPS
==============================
Custom analysis code and MD parameter files related to manuscript "Programmable de novo designed coiled coil-mediated phase separation in mammalian cells". The code in this repository are under the MIT License.

## Molecular simulation software
We used GROMACS v2022.1 to run all molecular dynamics simulations, both single molecule and slab, for this study. The specific details of compilation and types of computers used are described in the manuscript both in Methods and Supplemental Methods. 

You may download GROMACS v2022.1 [at this link](https://manual.gromacs.org/2022.1/download.html), and you can reference the documentation for this specific version [at this link](https://manual.gromacs.org/2022.1/index.html).

## Description of contents

### Custom\_scripts
This folder contains the scripts to do the multimerization counting analysis which was used in Figure S5. Molecular dynamics trajectories and an associated topology file (`.pdb` or the like) are provided to `multimerization_analysis.py` which produces a *contact map* of all coil segments in multimers in all analyzed frames, and `contact_analysis.py` determines statistics about those multimers from the contact map, such as multimer lifetimes and the percentage of time that each individual coil is engaged in a multimer interaction, to name a few. These scripts were written specifically for analysis of simulation trajectories for this paper.

Other analyses like density profile and molecular cluster analyses are tools provided by GROMACS. 

### MD\_parameter\_files
This folder contains the `.mdp` files for the single molecule and slab simulation procedures (at both 20 us and 40 us).

### Protein building
This folder contains scripts to do protein building, but *only for* proteins with parallel and antiparallel coil segments. Instructions and an example are provided. 

Instructions for making proteins that do not specify orientation (anything that is *not* APPAP, APPAPAPPAP, or PPPPPPAAAA) can be found in a repository for a related paper. The repository is [linked here](https://github.com/dora1300/cc_llps_framework).

As described in the paper, once a protein is made, you can then run single molecule simulations on it using the appropriate `.mdp` files (described above) and then pack configurations into a box of desired density and size using `Packmol`.

### Topologies
This folder contains all of the topology files (`.itp` and `.top`) for all of the proteins described in this manuscript. Each protein pair is given its own folder. `.top` files are predesigned for slab simulations.  


### Copyright

Copyright (c) 2023, Ram&#353;ak et al.
