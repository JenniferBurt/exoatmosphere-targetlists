# exoatmosphere-targetlists
Repo for [Burt et al. 2025 paper](https://arxiv.org/abs/2508.03801) on constructing representative target lists for exoplanet atmosphere characterization surveys

This repo is not especially well organized, but it contains all of the code used to construct the target lists, run the analysis, and make the figures presented in the paper. 

The MassRadiusRelation directory contains the code and input list of exoplanets with both masses and radii known to better than 50% precision that were used to create a mass-radius relation using [MRExo](https://shbhuk.github.io/mrexo/) package, which is then used to predict the masses of both confirmed planets and planet candidates that do not yet have measured masses.

The TargetListCreation directory contains the input lists of known planets (from the exoplanet archive), current TOIs (from MIT's TEV) and current KOIs (from the Exoplanet Archive), along with the TargetListCreation.ipynb notebook which carries out all of the steps for combining those input target lists and generating the list of planets and planet candidates that we deem as "viable" targets for exoatmospheric surveys.

The main directory contains the the resulting list of all viable targets (RepPlanets_Target_List_Full_May2025_3NightCut.csv) the lists of the 750 selected transmission targets (for both the known planets only case and the known planets + planet candidates case) and the lists of the 150 selected emission spectroscopy targets (again for both the known planets only case and the known planets + planet candidates case).  The RepPlanets_May2025.ipynb notebook contains the code used for all analysis and figure making within the paper -- some of it requires tweaking by hand (e.g. setting the V magnitude cut off used to assign targets to RV follow up telescopes) but for the most part it can be run as is. 

Note: the code could be improved in numerous ways to make things more efficient / less repetative (some day I will actually make use of python functions) but for now it is provided 'as is' and without plans for significant upgrades. Community members are welcome to make use of these results under the GPL-3.0 license.
