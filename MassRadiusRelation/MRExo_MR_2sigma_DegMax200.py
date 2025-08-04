import os, sys
from astropy.table import Table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import shutil

from mrexo.mle_utils_nd import InputData, MLE_fit
from mrexo.fit_nd import fit_relation
from mrexo.plotting_nd import Plot2DJointDistribution, Plot2DWeights, Plot1DInputDataHistogram
import matplotlib.pyplot as plt

t = pd.read_csv(r'C:\Users\skanodia\Documents\GitHub\mrexo\sample_scripts\JenARIELRuns\MassRadiusStellarMass_2sigma.csv')

# Mask NaNs
#t = t[~np.isnan(t['pl_insolerr1'])]
#t = t[~np.isnan(t['pl_bmasse'])]

# Define bounds in different dimensions
RadiusBounds = None #[0, 25]# None# [0, 100]
MassBounds = None# [0, 6000]
InsolationBounds = None# [0.01, 5000]
StellarMassBounds = None# [0.2, 1.2]

# Measurements with very small errors are set to NaN to avoid integration errors
t['st_masserr1'][t['st_masserr1'] < 0.005] = np.nan
t['st_masserr2'][t['st_masserr2'] < 0.005] = np.nan

if RadiusBounds is not None:
        t = t[(t.pl_radius > RadiusBounds[0]) & (t.pl_radius < RadiusBounds[1])]

if MassBounds is not None:
        t = t[(t.pl_mass > MassBounds[0]) & (t.pl_mass < MassBounds[1])]

if InsolationBounds is not None:
        t = t[(t.pl_insol > InsolationBounds[0]) & (t.pl_insol < InsolationBounds[1])]

if StellarMassBounds is not None:
        t = t[(t.st_mass > StellarMassBounds[0]) & (t.st_mass < StellarMassBounds[1])]

# Remove particular planets
RemovePlanets = ['Kepler-54 b', 'Kepler-54 c']
t = t[~np.isin(t.pl_name, RemovePlanets)]


#Build Input Dictionaries
# In Earth units
Mass = np.array(t['pl_mass'])
# Asymmetrical errorbars
MassUSigma = np.array(abs(t['pl_masserr1']))
MassLSigma = np.array(abs(t['pl_masserr2']))

Radius = np.array(t['pl_radius'])
# Asymmetrical errorbars
RadiusUSigma = np.array(abs(t['pl_radiuserr1']))
RadiusLSigma = np.array(abs(t['pl_radiuserr2']))

StellarMass = np.array(t['st_mass'])
StellarMassUSigma = np.array(t['st_masserr1'])
StellarMassLSigma = np.array(t['st_masserr2'])

#Insolation = np.array(t['pl_insol'])
#InsolationUSigma = np.array(t['pl_insolerr1'])
#InsolationLSigma = np.array(t['pl_insolerr2'])

# Let the script pick the max and min bounds, or can hard code those in. Note that the dataset must fall within the bounds if they are specified.
Max, Min = np.nan, np.nan

# Define input dictionary for each dimension
RadiusDict = {'Data': Radius, 'LSigma': RadiusLSigma,  "USigma":RadiusUSigma, 'Max':Max, 'Min':Min, 'Label':'Radius ($R_{\oplus}$)', 'Char':'r'}
MassDict = {'Data': Mass, 'LSigma': MassLSigma, "USigma":MassUSigma,  'Max':Max, 'Min':Min, 'Label':'Mass ($M_{\oplus}$)', 'Char':'m'}
#StellarMassDict = {'Data': StellarMass, 'LSigma': StellarMassLSigma, "USigma":StellarMassUSigma, 'Max':Max, 'Min':Min, 'Label':'Stellar Mass (M$_{\odot}$)', 'Char':'stm'}
#InsolationDict = {'Data': Insolation, 'LSigma': InsolationLSigma, "USigma":InsolationUSigma, 'Max':Max, 'Min':Min,  'Label':'Pl Insol ($S_{\oplus}$)', 'Char':'insol'}

# 2D fit with planetary radius and mass
InputDictionaries = [RadiusDict, MassDict]
DataDict = InputData(InputDictionaries)
ndim = len(InputDictionaries)

RunName = '2Sigma_MR_Planets_DegMax200'
save_path = os.path.join('./TestRuns',  RunName)

#Use the crossvalidation method to set the number of degrees in each fitting axis and allow for asymmetric degree values across dimensions
outputs= fit_relation(DataDict, select_deg='cv', save_path=save_path, degree_max=200, cores=50, SymmetricDegreePerDimension=True, NumMonteCarlo=0, NumBootstrap=0)

_ = Plot1DInputDataHistogram(save_path)

if ndim==2:
	_ = Plot2DJointDistribution(save_path)
    _ = Plot2DWeights(save_path)
