import numpy as np

#______________________________________________________________________________

def RVdataSelect(allPlanets, verbose=False):
  '''
   Pick out the RV-detected systems from the overall set of real planets
  '''

#  print allPlanets.keys()

  RVdata={'semia':[],'msini':[]}

  nplanets=len(allPlanets['pl_name'])
#  print 'nplanets',nplanets,len(allPlanets['pl_msinie']), \
#        len(allPlanets['pl_orbsmax'])

  for i in range(nplanets):
    if allPlanets['pl_discmethod'][i]=='Radial Velocity':
      if not allPlanets['pl_orbsmax'][i]:        
        if verbose:
          print('ERROR: semi-major axis is blank for RV planet', \
                allPlanets['pl_name'][i])
      elif not allPlanets['pl_msinie'][i]:
        if verbose:
          print('ERROR: Msini is blank for RV planet', \
                allPlanets['pl_name'][i])
      else:      
        RVdata['semia'].append(allPlanets['pl_orbsmax'][i])
        RVdata['msini'].append(allPlanets['pl_msinie'][i])
    else:      
      if allPlanets['pl_msinie'][i]:
        if verbose:
          print('non-RV-discovery with Msini value', \
                allPlanets['pl_name'][i], \
                allPlanets['kepler_name'][i])
      
  return RVdata
#______________________________________________________________________________

def onlyConfirmed(allPlanets):

  confirmedPlanets={}
  for key in allPlanets:
    confirmedPlanets[key]=[]
    
  for i in range(len(allPlanets['pl_name'])):
    if allPlanets['pl_name'][i]:
      for key in allPlanets:
        confirmedPlanets[key].append(allPlanets[key][i])

      if allPlanets['koi_disposition'][i]=='CANDIDATE':
        print('ERROR: candidate with confirmed name', \
              allPlanets['pl_name'][i])
    else:
      if allPlanets['koi_disposition'][i]!='CANDIDATE':
        print('ERROR: confirmed with no name?', \
              allPlanets['koi_disposition'][i])
  return confirmedPlanets
#______________________________________________________________________________

def checkDiff(observations,model,varName):
  if synthPop:
#    print 'comparing two arrays',len(observations),len(model)

    obsValues=selectValues(observations)
      
    D,p=scipy.stats.ks_2samp(obsValues,array(model))
                               
    print(' K-S test p-value:',p,' ('+varName+')')
  return
#______________________________________________________________________________

def selectValues(inarray):
  '''
  Pick out the values of the array that are defined.
  '''  
  out=[]
  for i in range(len(inarray)):
    if not isinstance(inarray[i],float):
      pass
    else:
      out.append(inarray[i])

  return numpy.array(out)
#______________________________________________________________________________

# data is a mix of float values and '' for missing data.
# fill in blank errors with zeros and return a float array.
#
def cleanErrors(data,param):

  print('cleaning:',param)
  for i in range(len(data['name'])): 
#    print i,param,data[param+'err1'][i]
    if data[param+'err1'][i]=='':
      data[param+'err1'][i] = np.nan
      if data[param+'err2'][i]!='':
        exit('ERROR: only first error blank for '+param)
      data[param+'err2'][i] = np.nan
    elif data[param+'err2'][i]=='':
      print('ARCHIVE ERROR: only one error blank for',param,data['name'][i])
      data[param+'err2'][i] = data[param+'err1'][i]

  data[param+'err1'] = np.array(data[param+'err1'])
  data[param+'err2'] = np.array(data[param+'err2'])

  return data
