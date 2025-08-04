def mergeTables(confirmedPlanets,KeplerList,verbose=False):

  allPlanets=mergeConfirmedCandidateTables(confirmedPlanets,KeplerList)

  if verbose:
    print('# of fields in allPlanets before redundancy removed',len(allPlanets))
    
# verify that all the arrays are the same length
  for key in allPlanets:
    if len(allPlanets[key])!=len(allPlanets['kepler_name']):
      print(' ERROR: array length is off for this key:',key,len(allPlanets[key]))


# merge all of the habitable zone information
#  - confirmed table gets priority over kepler table
#  - fill in blank fields where possible
#  - keep pl_insol,pl_eqt
#  - drop koi_insol,koi_teq (after merging their info into pl_insol,pl_eqt)
#  - do not recalculate values based on L_star (this is optionally done elsewhere)

# fill in blank Teq/insol values, if one is filled & other is empty
  allPlanets=fillHZinfo(allPlanets)

  allPlanets=mergeRedundantFields(allPlanets,'pl_rade','koi_prad')
  allPlanets=mergeRedundantFields(allPlanets,'pl_orbper','koi_period')
  allPlanets=mergeRedundantFields(allPlanets,'pl_orbincl','koi_incl')
  allPlanets=mergeRedundantFields(allPlanets,'pl_orbsmax','koi_sma')
  allPlanets=mergeRedundantFields(allPlanets,'pl_orbeccen','koi_eccen')
  allPlanets=mergeRedundantFields(allPlanets,'pl_eqt','koi_teq')
  allPlanets=mergeRedundantFields(allPlanets,'pl_insol','koi_insol')

# some mergers are more complicated, e.g. the redundancy for RJup/REarth
  RJupoREarth=69911./6371.
  MJupoMEarth=1.898e30/5.972e27
#  print 'Jupiter radius (Earth units)',RJupoREarth
#  print 'Jupiter mass   (Earth units)',MJupoMEarth
#  print
# (this optional check has to be before the second field is removed)
#  checkfields(allPlanets,'pl_rade','pl_radj',expectedRatio=RJupoREarth)
  allPlanets=mergeRedundantFields(allPlanets,'pl_rade','pl_radj',
                                  setRatio=RJupoREarth)

#  checkfields(allPlanets,'pl_masse','pl_massj',expectedRatio=MJupoMEarth)
  allPlanets=mergeRedundantFields(allPlanets,'pl_masse','pl_massj',
                                  setRatio=MJupoMEarth)

#  checkfields(allPlanets,'pl_msinie','pl_msinij',expectedRatio=MJupoMEarth)
  allPlanets=mergeRedundantFields(allPlanets,'pl_msinie','pl_msinij',
                                  setRatio=MJupoMEarth)

  if verbose:
    print() 
    print(list(allPlanets.keys()))
    print('# of fields in allPlanets after overlap removed',len(allPlanets))

# verify that all the arrays are the same length
  for key in allPlanets:
    if len(allPlanets[key])!=len(allPlanets['kepler_name']):
      print(' ERROR: array length is off for this key:',key,len(allPlanets[key]))

  print('Total number of planets (after overlap removed):', \
        len(allPlanets['pl_name']))
  print()
  return allPlanets
#______________________________________________________________________________

# this routine adds the two tables together, checking for duplicates based on RA/Dec
#  if the planet isn't listed in both tables, some fields are just left blank
#
# cleaning is NOT done here, e.g. merging two columns that are both for period,etc
#
def mergeConfirmedCandidateTables(confirmedPlanets,KeplerList,
                                  verbose=False):
  import copy

  nconfirm=len(confirmedPlanets['pl_msinij'])
  nkepler=len(KeplerList['kepler_name'])
          
  allPlanets=copy.deepcopy(confirmedPlanets)
  if verbose:
    print('confirmed-planet fields',list(allPlanets.keys()))
    print('Kepler-candidate fields',list(KeplerList.keys()))
    print()

# verify that the only overlapping field names are 'ra' and 'dec'
  for key in list(KeplerList.keys()):
    if key in list(allPlanets.keys()):
      if key!='ra' and key!='dec':
        print('NOTE: both tables have this same field name!',key)
    else:
# add the kepler field names to the combined list of fields
      allPlanets[key]=['']*nconfirm

#  loop through kepler list and if it's a new one, add it on
#    if it's not a new one, just add the kepler fields to the existing record
  for i in range(nkepler):
#    print 'check',allPlanets['koi_incl'][150]
    if KeplerList['koi_disposition'][i]=='CONFIRMED':
# this is a confirmed planet. it should be in both lists.

# the confirmed table doesn't include KOI or other Kepler identifier
# so the cross-matching has to be done by RA/Dec, it seems
      jmatch=-1
      closest=666.
      for j in range(nconfirm):
# make sure that the planet letters match, as well as the RA/Dec
        if allPlanets['pl_letter'][j]==KeplerList['kepler_name'][i][-1]:
#          print 'RA dec all',allPlanets['ra'][j],allPlanets['dec'][j]
#          print 'RA dec kep',KeplerList['ra'][i],KeplerList['dec'][i]
          offset2=(allPlanets['ra'][j]-KeplerList['ra'][i])**2 + \
                   (allPlanets['dec'][j]-KeplerList['dec'][i])**2
          if offset2 < closest:
            jmatch=j
            closest=offset2
#      print 'MATCH UP',i,jmatch,allPlanets['pl_letter'][jmatch], \
#            KeplerList['kepler_name'][i]
      if jmatch==-1:
        print('ERROR: no close match found')
      else:
        if closest>1.e-7:
          print('ERROR: found a match, but not close enough',closest, \
              allPlanets['ra'][jmatch]-KeplerList['ra'][i], \
              allPlanets['dec'][jmatch]-KeplerList['dec'][i])
#        print 'GOOD: match found',closest, \

#  copy over Kepler data into in the appropriate fields within allPlanets
      for key in list(KeplerList.keys()):
        if key!='ra' and key!='dec':
          if allPlanets[key][jmatch]!='':
            print('ERROR: overwriting a non-blank field', \
                  jmatch,key,allPlanets[key][jmatch])
          allPlanets[key][jmatch]=KeplerList[key][i]

# also, confirm that the values match, if they should.
#      print 'period check for overlapping tables', \
#            allPlanets['pl_orbper'][jmatch]/allPlanets['koi_period'][jmatch]
#      print 'insolation check for overlapping tables', \
#            allPlanets['kepler_name'][jmatch], \
#            allPlanets['pl_insol'][jmatch],allPlanets['koi_insol'][jmatch]


# add the kepler candidate info to the end of the list
    elif KeplerList['koi_disposition'][i]=='CANDIDATE':      
# extend all the fields by 1 
      for key in list(allPlanets.keys()):
        allPlanets[key].append('')

# fill in the kepler data (only for kepler fields; it only has kepler table data)
      for key in list(KeplerList.keys()):
        allPlanets[key][-1]=KeplerList[key][i]

    else:
      print('ERROR: strange disposition',KeplerList['koi_disposition'][i])

  return allPlanets
#______________________________________________________________________________

def mergeRedundantFields(allPlanets,field1,field2,
                         setRatio=1.,
                         verbose=False):
  nplanets=len(allPlanets['kepler_name'])

  ncounts=[0]*4
  for i in range(nplanets):

    if allPlanets[field1][i]:
      if allPlanets[field2][i]:
        ncounts[0]+=1
        ratio=float(allPlanets[field1][i])/float(allPlanets[field2][i])
        if verbose:
          if ratio/setRatio>2. or ratio/setRatio<0.5:
            print(' WAY OFF!! ('+field1,field2+'): ', \
                  allPlanets['pl_name'][i], \
                  allPlanets[field1][i],allPlanets[field2][i])
          print('dropping overlapping data ('+field1,field2+'): ', \
                allPlanets[field1][i],allPlanets[field2][i])
      else:
        ncounts[1]+=1
#        print 'ok: only has field1 data'
    elif allPlanets[field2][i]:
      ncounts[2]+=1
      if setRatio!=1:
# this would spot Jupiter info passed into the Earth radius field. no such case
        print('moving field2 data into field1 using setRatio')
      allPlanets[field1][i]=allPlanets[field2][i]*setRatio
    else:
      ncounts[3]+=1
#      print 'both fields are blank'  

  if verbose:
    print('merger summary',field1,field2, \
          '  [both,just1,just2,neither]=',ncounts)

  del allPlanets[field2]

  return allPlanets
#______________________________________________________________________________

#
# if there is an insolation but no equilibrium temperature, or vice-verse,
#   fill in the blank insolation/Teq value
#
def fillHZinfo(allPlanets):
  nplanets=len(allPlanets['kepler_name'])

  Albedo=0.3
# asdf: use zero albedo, to be consistent with rest of TESS data
  Albedo=0.
  Temperature1AU1LSun=278.6
  
  for i in range(nplanets):
    if allPlanets['pl_insol'][i] and allPlanets['pl_eqt'][i]:
#      print 'albedo check for confirmed', \
#            1. - (allPlanets['pl_eqt'][i]/276.5)**4/allPlanets['pl_insol'][i]
      pass
    elif allPlanets['pl_insol'][i]:
#      print 'filling in Teq for confirmed with insolation'
      allPlanets['pl_eqt'][i]=Temperature1AU1LSun*((1.0-Albedo)
                                *allPlanets['pl_insol'][i])**0.25
    elif allPlanets['pl_eqt'][i]:
#      print 'filling in insolation for confirmed with Teq'
      allPlanets['pl_insol'][i]=(allPlanets['pl_eqt'][i] 
                                 /Temperature1AU1LSun)**4 /(1.-Albedo)

#    if allPlanets['pl_insol'][i] and allPlanets['pl_eqt'][i]:
#      print 'albedo re-check for confirmed', \
#            1. - (allPlanets['pl_eqt'][i]/276.5)**4/allPlanets['pl_insol'][i]

    if allPlanets['koi_insol'][i] and allPlanets['koi_teq'][i]:
#      print 'albedo check for Kepler', \
#            1. - (allPlanets['koi_teq'][i]/279)**4/allPlanets['koi_insol'][i]
      pass
    elif allPlanets['koi_insol'][i]:
#      print 'filling in Teq for Kepler with insolation'
      allPlanets['koi_teq'][i]=Temperature1AU1LSun*((1.0-Albedo)
                                *allPlanets['koi_insol'][i])**0.25
    elif allPlanets['koi_teq'][i]:
#      print 'filling in insolation for Kepler with Teq'
      allPlanets['koi_insol'][i]=(allPlanets['koi_teq'][i] 
                                  /Temperature1AU1LSun)**4 /(1.-Albedo)
#    if allPlanets['koi_insol'][i] and allPlanets['koi_teq'][i]:
#      print 'albedo re-check for Kepler', \
#            1. - (allPlanets['koi_teq'][i]/279)**4/allPlanets['koi_insol'][i]

  return allPlanets
#______________________________________________________________________________

#______________________________________________________________________________

def checkfields(allPlanets,field1,field2,expectedRatio=1.):
  nplanets=len(allPlanets['kepler_name'])

  acc=1.03
  for i in range(nplanets):
    if allPlanets[field1][i]:
      if allPlanets[field2][i]:
        ratio=float(allPlanets[field1][i])/float(allPlanets[field2][i])
        if ratio/expectedRatio>acc or \
               ratio/expectedRatio<1./acc:            
          print('ratio is off ('+field1,field2+') ',ratio,ratio/expectedRatio, \
                allPlanets['pl_name'][i])
#      else:
#        print 'UHOH: blank field2 ('+field1,field2+') '
#    elif allPlanets[field2][i]:
#      print 'UHOH: blank field1 ('+field1,field2+') '

  return
#______________________________________________________________________________

#
# if there's no HabZone info (Teq,insol) calculate it from L_star
#
def calculateHZ(allPlanets):
  #nplanets=len(allPlanets['kepler_name'])
  nplanets=len(allPlanets['pl_name'])

  Albedo=0.3
  Temperature1AU1LSun=278.6
  
  for i in range(nplanets):
    if allPlanets['pl_insol'][i] and allPlanets['pl_eqt'][i]:
      pass
    elif allPlanets['pl_insol'][i]:
      print('ERROR: T_eq is blank when insol has a value')
    elif allPlanets['pl_eqt'][i]:
      print('ERROR: insolation is blank when T_eq has a value')
    else:
#      if allPlanets['st_lum'][i] and \
#             allPlanets['st_rad'][i] and allPlanets['st_teff'][i]:
#        lstar=10.**float(allPlanets['st_lum'][i])
#        rstar=allPlanets['st_rad'][i]
#        teff=allPlanets['st_teff'][i]
# mostly this is good, but there's a few that are way off, e.g. 7 Cma (K1III)
#        print 'Are Lstar,Teff,Rstar consistent?', \
#              allPlanets['pl_name'][i], \
#              lstar,rstar,teff,'  ',lstar/rstar**2/(teff/5777)**4

      if allPlanets['st_lum'][i] or \
             (allPlanets['st_rad'][i] and allPlanets['st_teff'][i]):

        if allPlanets['st_lum'][i]:
          lstar=10.**allPlanets['st_lum'][i]
        else:
          rstar=allPlanets['st_rad'][i]
          teff=allPlanets['st_teff'][i]
          lstar=rstar**2 *(teff/5777)**4


        if allPlanets['pl_orbsmax'][i]:
          r_AU=allPlanets['pl_orbsmax'][i]        
          insolation=lstar/r_AU**2
          Teq=Temperature1AU1LSun*((1.0-Albedo)*insolation)**0.25

#          print 'filling in T_eq and insol using L_star,r_AU',lstar,r_AU, \
#                insolation,Teq

          allPlanets['pl_insol'][i]=insolation
          allPlanets['pl_eqt'][i]=Teq

# do some HabZone consistency checks
          if insolation>0.319 and insolation<1.78:
            if Teq<191.5 or Teq>294.2:
              print('INCONSISTENCY: good in just insol', \
                  allPlanets['pl_name'][i],allPlanets['kepler_name'][i], \
                  allPlanets['pl_insol'][i],allPlanets['pl_eqt'][i])
#            else:
#              print '  this is HZ planet!',allPlanets['pl_name'][i]
          else:
            if Teq>191.5 and Teq<294.2:
              print('INCONSISTENCY: good in just Teq', \
                    allPlanets['pl_name'][i],allPlanets['kepler_name'][i], \
                    allPlanets['pl_insol'][i],allPlanets['pl_eqt'][i])
#            else:
#              print 'not in the HZ'

#        else:
#          print 'no semi-major axis though',allPlanets['pl_name'][i]
                           
#      else:
#        print 'nope. blank', \
#              allPlanets['st_lum'][i], \
#              allPlanets['st_rad'][i],allPlanets['st_teff'][i]
        
  return allPlanets
#______________________________________________________________________________

#______________________________________________________________________________

#______________________________________________________________________________
