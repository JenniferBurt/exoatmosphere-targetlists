def wolfgangMass(R_Earth):

  if R_Earth<4.:
    M_Earth=2.7*R_Earth**1.3
  else:
    M_Earth=666.e10
    
  return M_Earth

def traubMass(radiusEarth):
  if radiusEarth==0:
    exit('ERROR: zero radius in Radius-to-Mass conversion')
  
# Traub2011 formula, modified to enforce Earth/Jupiter fit
  r0=0.375
  r1=11.
  r1earlyCut=10.89
  m1=1000.
#  m1=2.e30/6.e27
  w=1.5  
  if radiusEarth > r1earlyCut:
#for radius larger than Jupiter, just assume Jupiter mass I guess. not good.
    massEarth=2.e30/6.e27

# much better to spread out the masses over some range
# so that they can be seen separately on mass-metal plot
# Weiss 2013 failed, so just pick arbitrary line
    massEarth=radiusEarth/r1 *2.e30/6.e27

#for planets smaller than Earth, assume Earth density
#  (so that the distribution is continuous; no breaks)
  elif radiusEarth < 1:
    massEarth=radiusEarth**3
  else:
# regular formula:
    massEarth=m1*10.**(-w*((r1-radiusEarth)/(radiusEarth-r0))**0.25)

  return massEarth
