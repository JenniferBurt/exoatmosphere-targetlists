import numpy as np

def massMetalRelationDisp(logmetStar,Mp):

  exit('are you sure you want scatter in the planet metallicity?')
  
  logmet=massMetalRelation(logmetStar,Mp)

#  dispersion=0.5
# let's try a lower dispersion, for testing at least
#  dispersion=0.1

  dispersion=0.3
  logmet+=random.gauss(0.,dispersion)

  return logmet 
#______________________________________________________

def massMetalRelation(logmetStar,Mp):


  slope=-1.0
#  intercept=1.0 + np.log10(1.898e30/5.972e27)
#  print 'intercept',intercept
  maxMetal=2.
  Mpivot=1.
  intercept=maxMetal - slope*Mpivot
#  print 'intercept',intercept

# Mp is in Earth masses. convert to Jupiters
# no! actually, don't convert it
#  MJup=Mp*5.972e27/1.898e30

#  logmet=logmetStar + intercept + slope*np.log10(Mp)
#  logmet=min(maxMetal,logmet)
# 8/10/16 oops, I think this is the problem I've been looking for!!
  logmet=intercept + slope*np.log10(Mp)
  logmet=min(maxMetal,logmet)
  logmet+=logmetStar

#  print 'Mp,logmet',Mp,logmet
#  print

#  print 'type check',type(logmet)
  return logmet 
#______________________________________________________

def randomStarMetal():

  exit('are you sure you want random stellar metallicity?')

# this is from my excel check of Hinkel's Hypatia catalog
#  logmetStar=0.06 + 0.29*numpy.random.randn(1)
#  logmetStar=0.06 + 0.29*random.gauss(0.,1.)

# from Kepler-detection-based (Buchhave 2011)
  logmetStar=-0.01 + 0.25*random.gauss(0.,1.)

  return logmetStar
#______________________________________________________

def randomCtoO():

  exit('are you sure you want random C/O?')
# this is from my excel check of Hinkel's Hypatia catalog
#  logCtoO=-0.13 + 0.19*numpy.random.randn(1)
#  logCtoO=-0.13 + 0.19*random.gauss(0.,1.)

# this is motivated by Fortney's argument that C>O is rare
# he gets 1-5% and suggests even lower
# let's just stick with 5% C/O>1,
#   in order to see how well FINESSE can do with some oddballs
# this gives 4.8% with C>O
  logCtoO=-0.2 + 0.12*random.gauss(0.,1.)

# reminder: solar is -0.26
#  we seem to be below average

  return logCtoO
#______________________________________________________
