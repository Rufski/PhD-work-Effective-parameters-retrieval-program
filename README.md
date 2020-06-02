# PhD-work-Effective-parameters-retrieval-program

## In a nutshell
This program is designed to take as an input the S-parameters generated by a simulation through the software CST Microwave, and extract the permittivity, permeability, impedance, refractive index, figure of merit, transmission and reflection parameters of the simulated material, outputting a set of plots of these parameters over a specified range of frequency.

The algorithm is based on the following paper:
Hsieh, Feng-Ju, and Wei-Chih Wang. [“Full extraction methods to retrieve effective refractive index and parameters of a bianisotropic metamaterial based on material dispersion models.”](https://aip.scitation.org/doi/full/10.1063/1.4752753?casa_token=xHGlMD94FbIAAAAA:YY1Ut2BzOVvrJ2qaQ4nMWqiqxmrBD1l0O9t8Xw53Yyu23K_guoP_HquBqAJgzXakLQQ6yrj8ZQE) Journal of Applied Physics 112.6 (2012): 064907.

At times, the following paper has also been used:
Chen, Xudong, et al. [“Robust method to retrieve the constitutive effective parameters of metamaterials.”](https://journals.aps.org/pre/pdf/10.1103/PhysRevE.70.016608?casa_token=wiemJYko8UIAAAAA%3AUivAP2Ai1PFI3QWCJXhM4SQNVA4Jrnw00TD1ZYq_kmcPPaWSWoHZg30TKz7d2ue_n-eBoHKt-Hiz_g) Physical Review E 70.1 (2004): 016608.

## Tools involved

## Input files
4 files names S11a.txt, S11p.txt, S21a.txt, S21p.txt containing the transmission (S21) and reflection (S11) amplitude (subscript a) and phase (subscript p) generated by CST Microwave simulation.

## Output files
9 graphs plotting the effective parameters mentioned in the first paragraph over the range of frequency covered by the S-parameter input files.

## Parameters to adjust within the program before running
frequnit, lengthunit, L10, L20, SlabThick, L1a, L2a.
