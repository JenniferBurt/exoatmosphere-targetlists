import numpy as np
import os

#______________________________________________________________________________
  
def readArchiveTables(params):
  directory=params['archiveDir']
  if directory[-1]!='/':
    directory=directory+'/'
  confirmedFilename=params['confirmedDataFile']
  keplerFilename=params['keplerDataFile']
  
  print('loading real planet data from directory:',directory)

# FIRST, load in the confirmed planet table

# optionally select a subset of the possible columns
#  (drop the variable or leave it blank for all columns)
  fieldList=params['confirmedDataFields']
#  fieldList=[]
  confirmedPlanets=readConfirmedPlanets(directory,confirmedFilename, \
                                        desiredFields=fieldList)
#  print 'confirmed exoplanet data successfully read in'
#  print ' # of fields: ',len(confirmedPlanets)
#  print ' # of planets:',len(confirmedPlanets['pl_hostname'])


# SECOND, load in the Kepler planet table

# optionally select a subset of the possible columns
#  (drop the variable or leave it blank for all columns)
  fieldList=params['keplerDataFields']
#  fieldList=[]
#  KeplerList=readKeplerPlanets(directory,keplerFilename, \
#                               desiredFields=fieldList)
  # DROP THE KEPLER LIST
  KeplerList = {'kepler_name':[]}
#  print 'kepler exoplanet data successfully read in'
#  print ' # of fields: ',len(KeplerList)
#  print ' # of planets:',len(KeplerList['kepler_name'])

#  print 'M sin i (Mjup)',confirmedPlanets['pl_msinij']
#  print 'M sin i (Mearth)',confirmedPlanets['pl_msinie']

#  print 'finished reading in the real planet data'
  print('  # confirmed, # kepler',len(confirmedPlanets['pl_name']), \
        len(KeplerList['kepler_name']))
  print()

  return confirmedPlanets,KeplerList
#______________________________________________________________________________

def readConfirmedPlanets(dir,filename, desiredFields=None):
  '''
  Download exoplanet data from the exoplanet archive.
  If data has already been downloaded, just open the saved file.

  Inputs:
  filename = name of the csv file (either an existing file or one to be created here)
  desiredFields = optional argument for selecting a subset of the possible columns
    (blank value means all data is returned)
  '''
  import csv

#  defaultfilename=filename+'.defaultColumns'
#  if os.access(dir+filename, os.R_OK):
  try:
    file=open(dir+filename,'r')
    print(' using pre-downloaded confirmed planet file:',filename)
  except:
    print(' '+filename,'does not exist')
    print(' downloading new data from archive:',filename)
    #os.system('wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=csv" -O '+dir+filename)
    sysCall = 'wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+pscomppars+&format=csv" -O '+dir+filename
    print(sysCall)
    os.system(sysCall)
    
    file=open(dir+filename,'r')
  csvfile=csv.reader(file)    

  try:
    header=next(csvfile)
  except:
    exit('ERROR: the file is blank.  Delete it!')
  #print header
  #exit()
  
# if the desired fields are not passed in, select everything
  if not desiredFields:
    desiredFields=header

# check that all of the desired field exist in this data
  missingfields=[]
  for field in desiredFields:
    if not field in header:
      print('WARNING: desired field does not exist',field)
      missingfields.append(field)
  if missingfields!=[]:
    exit('STOP: check the fields in params')
  
# reload the archive data, with specified (non-default) columns
  if missingfields:
    print('NOTE: some desired columns are not in the default table:',missingfields)
    print(' --> re-downloading with specified columns as:',filename)
    selectedColumns=''
    for field in desiredFields:
      selectedColumns=selectedColumns+field+','
    #print 'selectedColumns',selectedColumns
    #selectedColumns='pl_name,pl_bmassj'
    #os.system('wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=csv&select='+selectedColumns+'" -O '+dir+filename)
    # TRY TO UPDATE TO NEW COMPOSITE TABLE; ALSO USE TAP INSTEAD OF API!!
    #os.system('wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+'+selectedColumns+'+from+ps"')
    sysCall = 'wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+'+selectedColumns+'+from+pscomppars+&format=csv" -O '+dir+filename
    print(sysCall)
    os.system(sysCall)
    
    file=open(dir+filename,'r')
    csvfile=csv.reader(file)
    header=next(csvfile)
    
  data={}
  for field in desiredFields:
    data[field]=[]
  for line in csvfile:
    for field,value in zip(header,line):
      if field in desiredFields:
          try:
            data[field].append(float(value))
          except:
            data[field].append(value)

  for field in desiredFields:
    if not data[field]:
      print('WARNING: desired field not properly filled in:',field)
#    else:
#      print 'OK: field filled in:',field

#  exit('done loading and checking the data')
  return data
#______________________________________________________________________________

def readKeplerPlanets(dir,filename, desiredFields=None):
  '''
  Download exoplanet data from the exoplanet archive.
  If data has already been downloaded, just open the saved file.
  Inputs:
  filename = name of the csv file (either an existing file or one to be created here)
  desiredFields = optional argument for selecting a subset of the possible columns
    (blank value means all data is returned)
  '''
  import csv

  try:
    file=open(dir+filename,'r')
    print(' using pre-downloaded kepler planet file:',filename)
  except:
    candString="'CANDIDATE'"
    print(' '+filename,'does not exist')
    print(' downloading new data from archive:',filename)    
    os.system('wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&where=koi_pdisposition like '+candString+'&format=csv" -O '+dir+filename)
    file=open(dir+filename,'r')
  csvfile=csv.reader(file)

  try:
    header=next(csvfile)
  except:
    exit('ERROR: the file is blank.  Delete it!')
  
# if the desired fields are not passed in, select everything
  if not desiredFields:
    desiredFields=header

# check that all of the desired field exist in this data
  missingfields=[]
  for field in desiredFields:
#    print 'checking field',field
    if not field in header:
      print('WARNING: desired field does not exist:',field)
      missingfields.append(field)

# reload the archive data, with specified (non-default) columns
  if missingfields:
    print('NOTE: some desired columns are not in the default table:',missingfields)
    print(' --> re-downloading with specified columns as:',filename)
    selectedColumns=''
    for field in desiredFields:
      selectedColumns=selectedColumns+field+' '
    print('selectedColumns',selectedColumns)
# make sure to include the koi_pdisposition clause
#  or you get a bunch of 'FALSE POSITIVES'
    candString="'CANDIDATE'"
    os.system('wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&where=koi_pdisposition like '+candString+'&format=csv&select='+selectedColumns+'" -O '+dir+filename)

    file=open(dir+filename,'r')
    csvfile=csv.reader(file)
    header=next(csvfile)    
      
  data={}
  for field in desiredFields:
    data[field]=[]
  for line in csvfile:

# ignore all the false positives
#  6/8/15 this keeps only 4664 out of 8826
# no longer needed, since the wget was modified above
#  but might as well leave it in here just as a cross-check
    if 'FALSE POSITIVE' in line:
      print('dropping a false positive from kepler list')
    else:
      lineinfo=dict(list(zip(header,line)))

# optional conditional to drop kepler planets without radius
      if 0:
#      if (not lineinfo['koi_prad'] or lineinfo['koi_prad']=='0') \
#             and lineinfo['koi_disposition']=='CANDIDATE':
#        print 'TROUBLE: undefined planet:',lineinfo
        pass
      else:
#        print 'KEEPING: defined planet:',lineinfo

# this finds Kepler-295 d with blank radius.  must be dealt with later
#        if not lineinfo['koi_prad']:
#          print 'NOTE: undefined candidate confirmed?',lineinfo
        for field,value in zip(header,line):
          if field in desiredFields:
            try:
              data[field].append(float(value))
            except:
              data[field].append(value)

# Do some validation of the archive data
  if 0:
    for mass,name in zip(data['pl_msinij'],
                         data['pl_hostname']):
      if mass==0.:
        pass
#      print 'TROUBLE: zero planet mass!',name

    for inc,type,name in zip(data['pl_orbincl'],
                             data['pl_discmethod'],
                             data['pl_hostname']):
      if inc:
        if float(inc)<75. or float(inc)>90.:
          pass
          print('NOTE: odd inclination for transiting planet:',inc,name)
      else:
# these values simply aren't in the published data. ah well.
        print('TROUBLE: no inclination for transit planet',inc,name)

# check for msini/m consistency
    for msini,mass,type,inc,letter,name in zip(data['pl_msinij'],
                                               data['pl_massj'],
                                               data['pl_discmethod'],
                                               data['pl_orbincl'],
                                               data['pl_letter'],
                                               data['pl_hostname']):
      if type=='Radial Velocity':
        if not msini:
          pass
#          print 'ERROR: no msini for an RV planet',name,letter,inc
#        else:
#          print 'ok, it has an m-sin-i value',name
# o.k. this check below is essentially the same as above
        if mass and not inc:
          print('ERROR: its transiting, but no inclination',name,letter)
      elif 'Transit' in type:
        if msini:
          pass
#          print 'NOTE: there is msini for a Transit planet',name,letter
 
    for msinij,letter,name in zip(data['pl_msinij'],
                                  data['pl_letter'],
                                  data['pl_hostname']):
      pass

    for field in desiredFields:
      if not data[field]:
        print('WARNING: desired field not properly filled in:',field)
#      else:
#        print 'OK: field filled in:',field
    
#  exit('done loading and checking the data')
  return data
#______________________________________________________________________________

def readFinesseTargets(filename):
  import csv,string
  
  dir='./'
  file=open(dir+filename,'rb')

  file=csv.reader(file,delimiter='|')

  header=next(file)
  for i in range(len(header)):
    header[i]=string.strip(header[i])

  data={}
  for field in header:    
    data[field]=[]
  for line in file:
    for field,value in zip(header,line):
      if string.strip(field):
#        print field,'value:',value
        try:
          data[field].append(float(value))
        except:
          data[field].append(value)

  if 'Teff_p' in list(data.keys()) and not 'Teff' in list(data.keys()):
    data['Teff']=data['Teff_p']

  return data

def readTESS(filename='tessPlanets.csv',dir='./tessSim/'):
  import csv,string
  
  file=open(dir+filename,'r')
  file=csv.reader(file)

  header=next(file)
  for i in range(len(header)):
    header[i]=string.strip(header[i])
  
  data={}
  for field in header:    
    data[field]=[]
  for line in file:
    for field,value in zip(header,line):
      if string.strip(field):
#        print field,'value:',value
# float() doesn't work for the 'name' field
        try:
          data[field].append(float(value))
        except:
          data[field].append(value)
  for field in header:
    data[field]=np.array(data[field])
    
  return data
#______________________________________________________________________________

def readTargets(filename,dir='./'):
  import csv,string

  file=open(dir+filename,'r')
  file=csv.reader(file,delimiter='|')

  header=next(file)
  for i in range(len(header)):
    header[i]=string.strip(header[i])
  
  data={}
  for field in header:    
    data[field]=[]
  for line in file:
    for field,value in zip(header,line):
      if string.strip(field):
#        print field,'value:',value
# float() doesn't work for the 'name' field
        try:
          data[field].append(float(value))
        except:
          data[field].append(string.strip(value))
  
  for field in header:
    data[field]=np.array(data[field])

# the final '|' creates a blank field at the end.  remove it
  if '' in list(data.keys()):
    data.pop('')
        
  return data
#______________________________________________________________________________

def readBarclay(filename='barclayPlanets.csv',dir='./barclay18/'):
  import csv,string
  
  file=open(dir+filename,'r')
  file=csv.reader(file)

  header=next(file)
  for i in range(len(header)):
    header[i]=string.strip(header[i])
  
  data={}
  for field in header:    
    data[field]=[]
  for line in file:
    #print 'line',line
    Ncols = len(line)
    if Ncols!=33:
      print('STRANGE NUMBER OF COLUMNS',Ncols,line)
# glitch in the csv file, line 977:  whuzzup?
#      479106532,0.7765109763496892,14722.917360566487,0.10497802793043924,62.59598493425862,293.1137518229855
    else:
     for field,value in zip(header,line):
      if string.strip(field):
        #print field,'value:',value
        try:
          data[field].append(float(value))
        except:
          data[field].append(value)
    #print 'len check',len(data['TICID']),len(data['Vmag'])
    if len(data['TICID'])!=len(data['Vmag']):
      exit('ERROR: list appending trouble')

  for field in header:
    data[field]=np.array(data[field])
    #print 'len check',len(data[field]),field
  #print data['TICID'][3650],data['DEdeg'][3650],data['Kmag'][3650],data['Vmag'][3650]
  #exit()
  
  return data
#______________________________________________________________________________

#def readTESScandidates(params, filename='TESScandidateDownload.txt',
def readTESScandidates(params, filename='TOI_2021.12.16_16.36.23.csv',
                       desiredFields=None):
  import csv

  dir = params['archiveDir']
  if dir[-1] != '/':
    dir = dir + '/'

  #  defaultfilename=filename+'.defaultColumns'
  #  if os.access(dir+filename, os.R_OK):
  try:
    file=open(dir+filename,'r')
    print(' using pre-downloaded confirmed planet file:',filename)
  except:
    print(' '+filename,'does not exist')
    print(' downloading new data from archive:',filename)
    sysCall = 'wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+toi+&format=csv" -O '+dir+filename
    sysCall = 'wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+TOI+&format=csv" -O '+dir+filename
    print(sysCall)
    os.system(sysCall)
    
    file=open(dir+filename,'r')
  csvfile=csv.reader(file)    

  try:
    header=next(csvfile)
  except:
    exit('ERROR: the file is blank.  Delete it!')
  #print header
  
# if the desired fields are not passed in, select everything
  if not desiredFields:
    desiredFields=header

# check that all of the desired field exist in this data
  missingfields=[]
  for field in desiredFields:
    if not field in header:
      print('WARNING: desired field does not exist',field)
      missingfields.append(field)
  if missingfields!=[]:
    exit('STOP: check the fields in params')
  
# reload the archive data, with specified (non-default) columns
  if missingfields:
    print('NOTE: some desired columns are not in the default table:',missingfields)
    print(' --> re-downloading with specified columns as:',filename)
    selectedColumns=''
    for field in desiredFields:
      selectedColumns=selectedColumns+field+','
    #print 'selectedColumns',selectedColumns
    #selectedColumns='pl_name,pl_bmassj'
    #os.system('wget "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&format=csv&select='+selectedColumns+'" -O '+dir+filename)
    # TRY TO UPDATE TO NEW COMPOSITE TABLE; ALSO USE TAP INSTEAD OF API!!
    #os.system('wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+'+selectedColumns+'+from+ps"')
    sysCall = 'wget "http://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+'+selectedColumns+'+from+pscomppars+&format=csv" -O '+dir+filename
    print(sysCall)
    os.system(sysCall)
    
    file=open(dir+filename,'r')
    csvfile=csv.reader(file)
    header=next(csvfile)
    
  data={}
  for field in desiredFields:
    data[field]=[]
  for line in csvfile:
    for field,value in zip(header,line):
      if field in desiredFields:
          try:
            data[field].append(float(value))
          except:
            data[field].append(value)

  for field in desiredFields:
    if not data[field]:
      print('WARNING: desired field not properly filled in:',field)
#    else:
#      print 'OK: field filled in:',field

#  exit('done loading and checking the data')
  return data
#______________________________________________________________________________

