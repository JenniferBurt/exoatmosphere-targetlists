import numpy as np
import string
import csv
import random
random.seed(1234)

from params import Parameters
from readers import readArchiveTables
from mergeTables import calculateHZ
from selectData import cleanErrors
from relations import massMetalRelation
from MRrelation import traubMass
from calcMMW import calcMMW

# output pipe-separated or comma-separated file?
icsv = 1 # comma-separated
# icsv = 0 # pipe separated

# for a faster debugging run, don't calculate all the mean-molec weights
# iDebug = 1 # yes debug; no mmw
iDebug = 0 # no debug; yes mmw

Rgas = 8.314e7
G = 6.67e-8
REarth = 6.371e8
RSun = 6.957e10
MEarth = 5.972e27
SNRrenormFactor = REarth**3 / RSun**2 / MEarth / G * 1.e6 * Rgas

# print out all of the transiting planets, even those without mass
ifakemasses = 1

# blankRp = 66666.
blankRp = np.nan

#___________________________________________________

if __name__=='__main__':

  verbose = False
  verbose = True

  # set parameters in the 'params.py' file.  read them in here
  params = Parameters()


  # read in the real planet data
  allPlanets,KeplerList = readArchiveTables(params)

  # use Lstar to define HabZone, if it's blank
  allPlanets = calculateHZ(allPlanets)

  # fix some problems in the catalog
  #  these two guys are missing both mass and radius
  #
  # this guy is so famous, but tons of bad nulls in the default 2015 ref
  i = allPlanets['pl_name'].index('HD 189733 b')
  allPlanets['pl_bmasse'][i] = 369.
  allPlanets['pl_rade'][i] = 13.63
  #
  # this guy is a TTV inferred planet.  no transits
  i = allPlanets['pl_name'].index('Kepler-37 e')
  allPlanets['pl_bmasse'][i] = 1.e-3
  allPlanets['pl_rade'][i] = 1.e-3
  #
  # gees, a lot missing for this guy, despite fame & fortune
  i = allPlanets['pl_name'].index('HD 209458 b')
  #  print 'blanks, right?',allPlanets['pl_orbsmax'][i], \
  #        allPlanets['pl_eqt'][i], \
  #        allPlanets['pl_bmasse'][i] 
  allPlanets['pl_orbsmax'][i] = 0.047
  allPlanets['pl_eqt'][i] = 1450.
  allPlanets['pl_bmasse'][i] = 210.


#_________output known targets_________

  data = {}
  for key in allPlanets:
    data[key] = []


  # select only the transiting planets 
  for i in range(len(allPlanets['pl_name'])):
    if allPlanets['tran_flag'][i]:
      for key in allPlanets:
        data[key].append(allPlanets[key][i])

  nplanets = len(data['pl_name'])
  print('# of transiting planets',nplanets)

  desiredColumns = params['outputColumns']

  # initialize these columns, even though most are reassigned below
  for field in desiredColumns:
    if field in list(data.keys()):
      print('ERROR: field already exists in the archive data',field)
    data[field] = np.array([np.nan]*nplanets)

  for i in range(nplanets):
    if data['hostname'][i]+' '+data['pl_letter'][i] != \
           data['pl_name'][i]:
      print('strange naming',i, \
            data['hostname'][i],data['pl_letter'][i], \
            data['pl_name'][i])
    
    if not 'Transit' in data['discoverymethod'][i]:
      if verbose:
        print('not discovered by transit!  ',i, \
              data['pl_name'][i],data['discoverymethod'][i])

  # change the naming scheme and deal with empty desired columns
  data['name'] = data['pl_name']
  data['trnsmit'] = np.zeros(nplanets)
  data['emit'] = np.zeros(nplanets)
  data['real'] = np.zeros(nplanets) + 1.

  # this assignment is a little silly but is required
  #  (because the new column is NaN'd out above)
  data['RA'] = data['ra']
  data['Dec'] = data['dec']

  data['M_*'] = data['st_mass']
  data['R_*'] = data['st_rad']
  data['Teff_*'] = data['st_teff']
  #data['logMet_*'] = data['st_metfe']
  #data['hmag'] = np.array(data['st_h'])
  data['logMet_*'] = data['st_met']
  data['hmag'] = np.array(data['sy_hmag'])
  data['hmag'][np.where(data['hmag']=='')] = np.nan
  data['hmag'] = np.array(data['hmag']).astype(float)
  # the ones in the galactic bulge don't have any H band info
  for i in range(nplanets):
    if 'OGLE-TR' in data['name'][i] or \
           'SWEEPS' in data['name'][i]:
      data['hmag'][i] = 16.666


  data['jmag'] = np.array(data['sy_jmag'])
  data['jmag'][np.where(data['jmag']=='')] = np.nan
  data['jmag'] = np.array(data['jmag']).astype(float)

  data['vmag'] = np.array(data['sy_vmag'])
  data['vmag'][np.where(data['vmag']=='')] = np.nan
  data['vmag'] = np.array(data['vmag']).astype(float)

  data['ecc'] = np.array(data['pl_orbeccen'])
  data['ecc'][np.where(data['ecc']=='')] = np.nan
  data['ecc'] = np.array(data['ecc']).astype(float)

  data['omega'] = np.array(data['pl_orblper'])
  data['omega'][np.where(data['omega']=='')] = np.nan
  data['omega'] = np.array(data['omega']).astype(float)

  data['M_p'] = data['pl_bmasse']
  data['R_p'] = data['pl_rade']
  data['Teff_p'] = data['pl_eqt']
  data['a_p'] = data['pl_orbsmax']
  data['Period'] = data['pl_orbper']
  data['T_transit'] = data['pl_tranmid']

  # include errors
  #  if error fields are blank, fill with zeros ig
  #  also, make sure both errors are zero/non-zero (there's some archive bugs)
  #  also, convert to array
  if 'st_raderr1' in list(data.keys()):
    data = cleanErrors(data,'st_rad')
    data = cleanErrors(data,'st_teff')
    data = cleanErrors(data,'pl_rade')
    data = cleanErrors(data,'pl_orbsmax')
    data = cleanErrors(data,'pl_bmasse')
    data = cleanErrors(data,'pl_orbper')
    data = cleanErrors(data,'pl_tranmid')
    data = cleanErrors(data, 'pl_orbeccen')
    data = cleanErrors(data, 'pl_orblper')

    data['R_p_err'] = (data['pl_radeerr1'] - data['pl_radeerr2'])/2.
    data['a_p_err'] = (data['pl_orbsmaxerr1'] - data['pl_orbsmaxerr2'])/2.
    data['R_*_err'] = (data['st_raderr1'] - data['st_raderr2'])/2.
    data['Teff_*_err'] = (data['st_tefferr1'] - data['st_tefferr2'])/2.
    data['M_p_err'] = (data['pl_bmasseerr1'] - data['pl_bmasseerr2'])/2.
    data['Period_err'] = (data['pl_orbpererr1'] - data['pl_orbpererr2'])/2.
    data['T_transit_err'] = (data['pl_tranmiderr1'] - data['pl_tranmiderr2'])/2.
    data['ecc_err'] = (data['pl_orbeccenerr1'] - data['pl_orbeccenerr2']) / 2.
    data['omega_err'] = (data['pl_orblpererr1'] - data['pl_orblpererr2']) / 2.
  
  data['SNRfactor'] = np.zeros(nplanets)
  data['SNRfactorEmission'] = np.zeros(nplanets)

  data['dur1'] = data['pl_trandur']
  data['mmw'] = np.zeros(nplanets) + 2.5

  data['distance'] = data['sy_dist']

  data['realMp'] = [1]*nplanets

  for i in range(nplanets):
    # first check to see if the mass is actually an upper limit
    if data['pl_bmasselim'][i]!='':
      #print 'lim M',data['pl_bmasselim'][i],data['M_p'][i]
      if data['pl_bmasselim'][i]==1:
        data['M_p'][i] = ''
      elif data['pl_bmasselim'][i]==0:
        pass
      else:
        exit('mass limiter flag problem')
        
    # fill in blank masses with roughly Solar-System relation
    if not data['M_p'][i]:
      if not data['R_p'][i]:
        print('trying to call traubMass for radius:',data['R_p'][i])
        print(' ',data['name'][i])
        print(' M',data['M_p'][i])
        print(' T',data['Teff_p'][i])
        data['R_p'][i] = 1.
        data['M_p'][i] = 1.
        exit('fix these archive bugs')
      else:
        missingMpFlag = 0.666/5.972e27*1.898e30
        missingMpFlag = 0.666
        if verbose:
          print('using traubMass formula:',data['name'][i], \
                data['R_p'][i])
        # let's keep the ones without masses, but flag them as fake mass
        if ifakemasses:
          data['M_p'][i] = traubMass(data['R_p'][i])
          data['realMp'][i] = 0
          #print 'filling in mass for index',i
        else:
          data['M_p'][i] = missingMpFlag

    # fill in blank stellar data with something Sunlike for now
    if not data['M_*'][i]:
      try:
        a = float(data['a_p'][i])
        P = float(data['Period'][i]/365.25)
        MstarKeplerian = a**3/P**2
        #print 'updating Mstar',MstarKeplerian,data['M_*'][i]
        data['M_*'][i] = MstarKeplerian
        #Mstar = data['M_*'][i]
        #print 'keplerian check',Mstar/a**3*P**2,Mstar,a,P
      except:
        data['M_*'][i] = 1.
        print('arbitrary Mstar',data['name'][i])
        
    if not data['R_*'][i]:
      if verbose:
        print('HEY NO RSTAR',data['name'][i])
        # oh! WASP-100 b is the only one missing Rstar. not bad!
      try:
        Lstar = 10.**float(data['st_lum'][i])
        print('   Lstar',data['name'][i],data['st_lum'][i])
        Tstar = float(data['Teff_*'][i])
        data['R_*'][i] = Lstar/(Tstar/5777)**4
      except:
        # approx guess for WASP-100
        if data['name'][i]=='WASP-100 b':
          data['R_*'][i] = 1.5
        else:
          print('no Lstar prob',data['name'][i],data['st_lum'][i])
          data['R_*'][i] = 1.      
    else:
      try:
        Lstar = 10.**float(data['st_lum'][i])
        Tstar = float(data['Teff_*'][i])
        Rstar = float(data['R_*'][i])
        lstar = (Tstar/5777)**4*Rstar**2
        if Lstar/lstar < 0.9 or Lstar/lstar > 1.1:
          if verbose:
            print('Lstar check',Lstar/lstar,data['name'][i], \
                  Lstar,Tstar,Rstar)
        # luminosity is way off for Kepler-105.
        #    Lstar = 4.0 in archive  off by 2.8!
        # kepler-24 is low L or maybe high R actually. don't know
        # (plus some others not as extremely off)
        # 11/4/16 looks like Kepler-105 has been fixed.
        #         oh wait actually Lstar is blank.
        #         maybe I was filling it in with junk before?
      except:
        if verbose:
          print('MISSING LSTAR ig',data['name'][i], \
            data['st_lum'][i],data['Teff_*'][i],data['R_*'][i])

    if not data['Teff_*'][i]:
      #print 'HEY NO TSTAR',data['name'][i]
      try:
        Lstar = 10.**float(data['st_lum'][i])
        #print '   Lstar',data['name'][i],data['st_lum'][i]
        Rstar = float(data['R_*'][i])
        data['Teff_*'][i] = 5777.*(Lstar/Rstar**2)**0.25
      except:
        print('PROB: no Lstar or Tstar',data['name'][i], \
              data['st_lum'][i],data['Teff_*'][i],'  R_*:',data['R_*'][i])
        data['Teff_*'][i] = 6000.

    # Lstar isn't saved, but fill in anyway for checking below
    if not data['st_lum'][i]:
      if verbose:
        print('HEY NO LSTAR',data['name'][i])
      try:
        Rstar = float(data['R_*'][i])
        Tstar = float(data['Teff_*'][i])
        Lstar = (Tstar/5777)**4 * Rstar**2
        data['st_lum'][i] = log10(Lstar)
        #print ' yes filled Lstar',data['name'][i],data['st_lum'][i]
      except:
        print(' not filled Lstar',data['name'][i],data['st_lum'][i])
        
    if not data['a_p'][i]:
      try:
        Mstar = float(data['M_*'][i])
        P = float(data['Period'][i])/365.25
        data['a_p'][i] = (Mstar*P**2)**(1./3.)
        a = data['a_p'][i]
        #print 'keplerian fix check',Mstar/a**3*P**2,'  ',Mstar,a,P
      except:
        data['a_p'][i] = np.nan
        print('PROB: empty a_p',data['name'][i])
    else:
      try:
        P = float(data['Period'][i])/365.25
        Mstar = float(data['M_*'][i])
        a = data['a_p'][i]
        newAp = (Mstar*P**2)**(1./3.)
        #print 'keplerian check',newAp/a,Mstar,a,P
      except:
        pass
      
    if not data['Period'][i]:
      try:
        Mstar = float(data['M_*'][i])
        a = float(data['a_p'][i])
        data['Period'][i] = (a**3/Mstar)**0.5 *365.25
        P = data['Period'][i]/365.25
        #print 'keplerian fix check',Mstar/a**3*P**2,'  ',Mstar,a,P
      except:
        data['Period'][i] = np.nan
        print('PROB: empty Period',data['name'][i])
    else:
      try:
        P = float(data['Period'][i])/365.25
        Mstar = data['M_*'][i]
        a = data['a_p'][i]
        newAp = (Mstar*P**2)**(1./3.)
        #print 'keplerian check',newAp/a,Mstar,a,P
      except:
        pass
    
    if not data['Teff_p'][i]:
      try:
        Lstar = 10.**float(data['st_lum'][i])
        #Rstar = data['R_*'][i]
        #Tstar = data['Teff_*'][i]
        a = float(data['a_p'][i])
        albedo = 0.
        TBB = 278.6*((1.-albedo)*Lstar/a**2)**0.25
        if verbose:
          print('filling in T_planet',TBB,data['name'][i])
        data['Teff_p'][i] = TBB
      except:
        print('PROB: no temperature for planet',data['name'][i], \
              ' L =  ',data['st_lum'][i], \
              ' a =  ',data['a_p'][i])
        data['Teff_p'][i] = np.nan
    else:
# check the albedo used for the Teff calculation
#  check two cases 1) Lstar and 2) Rstar+Tstar
      try:
        Lstar = 10.**float(data['st_lum'][i])

        Rstar = float(data['R_*'][i])
        Tstar = float(data['Teff_*'][i])
        Lstar2 = (Tstar/5777)**4 * Rstar**2

        a = float(data['a_p'][i])
        T = float(data['Teff_p'][i])
        albedo  = 1. - (T/278.6)**4 /Lstar  *a**2 
        albedo2 = 1. - (T/278.6)**4 /Lstar2 *a**2 
#        print 'L a T',Lstar,a,T
# asdf:
# *** perhaps fix the Teff to match albedo = 0 for all of these ?? ***
        if verbose:
          print('albedo from archive data',albedo,albedo2,' ',data['name'][i],Tstar)
      except:
        print('HUH? missing stuff ', \
              ' L =  ',data['st_lum'][i], \
              ' T =  ',data['Teff_p'][i], \
              ' a =  ',data['a_p'][i], \
              ' ',data['name'][i])

    # note that duration comes from the archive in days
    #  later it's converted to seconds
    if not data['dur1'][i]:
      try:
        P_days = float(data['Period'][i])
        a_cm = float(data['a_p'][i])*1.5e13
        Rstar_cm = float(data['R_*'][i])*7e10
        # assume maximum transit duration, I guess
        fracOrbit = 2.*Rstar_cm / (2.*3.14159*a_cm)         
        data['dur1'][i] = P_days * fracOrbit
#        print 'transit duration (days)',data['name'][i],data['dur1'][i]
# oof, some weird stuff here.
#  e.g. K2-11 b with 1.35 days duration
#     Montet info has Rstar~1, but Rstar = 5 in star info
# this might work better if a/R_* parameter read in from archive
      except:
        print('PROB: transit duration undefined:',data['name'][i])
#        data['dur1'][i] = 666./24./3600.
        data['dur1'][i] = np.nan

    # hmm, some oddballs here; but they get dropped later for some reason
    # so I don't see any 666 in the final list.
    if not data['R_p'][i]:
      print('STRANGE: theres no planet radius?!',data['name'][i])
      data['R_p'][i] = blankRp

    # calculate star and planet metallicity
    if not data['logMet_*'][i]:
      if verbose:
        print('no stellar metallicity for this one',i,data['name'][i])
      #data['logMet_*'][i] = randomStarMetal()
      data['logMet_*'][i] = 0

    data['logMet'][i] = massMetalRelation(data['logMet_*'][i],data['M_p'][i])
    # weird. massMetalRelation gives floats, but they're turned into strings
    # (because array was set up as 'missing'*N)
    #    print 'type check',type(data['logMet'][i])

    # calculate star and planet C/O ratio
    logCtoOsolar = -0.26
    #logCtoO = randomCtoO()
    logCtoO = logCtoOsolar

    data['logCtoO'][i] = logCtoO
    data['logCtoO_*'][i] = logCtoO

    # some distances are missing.  avoid strings
    # the archive really needs to update some of these, e.g. GJ 1214 at 15 pc
    if data['distance'][i]=='':
      data['distance'][i] = np.nan

    # some transit times are missing.  avoid strings
    if data['T_transit'][i]=='':
      data['T_transit'][i] = np.nan
  
  # can only make them into float arrays after the blanks filled in
  data['M_*'] = np.array(data['M_*']).astype(float)
  data['R_*'] = np.array(data['R_*']).astype(float)
  data['Teff_*'] = np.array(data['Teff_*']).astype(float)
  data['M_p'] = np.array(data['M_p']).astype(float)
  data['R_p'] = np.array(data['R_p']).astype(float)
  data['Teff_p'] = np.array(data['Teff_p']).astype(float)
  data['dur1'] = np.array(data['dur1']).astype(float) *24.*3600.
  data['distance'] = np.array(data['distance']).astype(float)
  
  # weirdly coming back from defining routine as a string
  data['logMet'] = np.array(data['logMet']).astype(float)
  data['logCtoO'] = np.array(data['logCtoO']).astype(float)

  # calculate log-g
  G = 6.67e-8
  data['logg_*'] = np.log10(G*data['M_*']*1.99e33 \
                          /(data['R_*']*6.957e10)**2)
  data['logg'] = np.log10(G*data['M_p']*5.972e27 \
                        /(data['R_p']*6.371e8)**2)

  # calculate the mean molecular weights
  for i in range(nplanets):
    Tiso = data['Teff_p'][i]
    logMet = data['logMet'][i]
    logCtoO = data['logCtoO'][i]
    Rp = data['R_p'][i]*6.371e8/7.1492e9
    Rstar = data['R_*'][i]
    #print 'Rp (jup), Rstar (solar)',Rp,Rstar
    Mp = data['M_p'][i]*5.972e27/1.898e30
    #print 'planet mass (Jup)',Mp
    G = 6.67e-8
    logg = np.log10(G*Mp*1.898e30/(Rp*7.1492e9)**2)

    #print 'logg (cgs)',logg
    if not iDebug:
      #print 'mmw inputs:',Tiso,logMet,logCtoO,Rp,Rstar,logg
      #print ' type check',type(logMet)
      mmw = calcMMW(Tiso,logMet,logCtoO,Rp,Rstar,logg)
      #mmw = 3.  # (fast assignment, just for debugging purposes)
      data['mmw'][i] = np.average(mmw)
      print('mmw!',i,nplanets,data['mmw'][i])
      if data['mmw'][i]==1:
        print('mmw trouble!',i,nplanets,data['mmw'][i])
        print(' T',Tiso)
        print(' Rp (Jup), Rstar (solar)',Rp,Rstar)
        print(' Mp (Jup), logg',Mp,logg)
        print(' met C/O',logMet,logCtoO)
        print()
        data['mmw'][i] = 3.33

  # 10/25/2016 change the normalization a bit so this = the figure of merit
  #  i.e. drop the -8 on magnitudes and add a factor of 2 to scale height
  #  SNR = 10.**(-(data['hmag']-8.)/5.)  
  SNR = 10.**(-data['hmag']/5.)  
  SNR = SNR * (data['R_p']/data['R_*'])**2
  # the scale height now includes the mean molecular weight!
  H = data['Teff_p'] * data['R_p']**2 / data['M_p'] / data['mmw']
  SNR = SNR * 2.*H / data['R_p']
  data['SNRfactor'] = SNR

  data['SNRfactor'] *= SNRrenormFactor

  data['spectral modulation'] = 2. * H * (data["R_p"] * 6378.14) / ((data["R_*"] * 695700.) ** 2.)

  data['spectral modulation [ppm]'] = data['spectral modulation']*(1e6)


  
  # old simple version - ratio of planet/star temperatures
  #  data['SNRfactorEmission'] = SNR * data['Teff_p']/data['Teff_*']
  # correct version - ratio of planet/star blackbodies
  # caveat - you have to choose a wavelength of interest
  #  let's try 2um
  # for very large wavelength, get the same result as before
  # refWave = 2.e-4   # this is 2 microns in cgs units
  refWave = 1.65e-4  # this is the middle of the H-band - updated by Rob Zellem
  refNu = 3.e10/refWave
  hpl = 6.626e-27
  boltz = 1.38e-16
  Tratio = data['Teff_p']/data['Teff_*']
  #  for i in range(10):
  #    wave = (i+2.)/3. 
  #    refNu = 3.e10/(wave*1.e-4)
  #    T = 1750
  #    print 'T,wave(um),BB',T,wave, \
  #          refNu**4/(np.exp(hpl*refNu/boltz/T) - 1.)
    
  BBp = 1./(np.exp(hpl*refNu/boltz/data['Teff_p']) - 1.)
  BBs = 1./(np.exp(hpl*refNu/boltz/data['Teff_*']) - 1.)
  BBfactor = BBp/BBs
  print('Tp',data['Teff_p'])
  print('Ts',data['Teff_*'])
  print('Tratio ',Tratio)
  print('BBratio',BBfactor)
  # 10/24/16  take out the H/R factor!! not needed for emission
  SNR = data['SNRfactor'] / (2.*H / data['R_p'])
  # 10/25/16 multiply by 1e4, otherwise not enough sig figs
  data['SNRfactorEmission'] = SNR * BBfactor * 1.e4

  # add the metallicity dispersion *after* the SNR estimatation
  # (it's not fair to know the metallicity before observing it)
  #  for i in range(nplanets): 
  #    logmet = massMetalRelationDisp(data['logMet_*'][i],data['M_p'][i])
  #    data['logMet'][i] = logmet
          

#_________________________CULLING________________________


  idrop = []
  for i in range(nplanets):
    T = data['Teff_p'][i]
    # convert from Earth units to Jupiter units
    Rp = data['R_p'][i]*6.371e8/7.1492e9
    Mp = data['M_p'][i]*5.972e27/1.898e30
    HR = T*Rp/Mp
    g = Mp/Rp**2

    # (maybe) drop planets without measured masses
    #  (or maybe include them with standard mass-radius relation)
    if data['M_p'][i]==missingMpFlag:
      print('dropping one that doesnt have a measured mass',data['name'][i])
      idrop.append(i)

    # drop some supposed transiting planets with no (default) radius 
    elif data['R_p'][i]==blankRp:
      print('dropping a planet with empty R_p',i,Mp,data['name'][i])
      idrop.append(i)
      
    # drop planets with low Temperature
    elif data['Teff_p'][i]<400.:
      print('dropping a planet with low temperature',i, \
        data['Teff_p'][i],data['name'][i])
      ###idrop.append(i)
      pass
    
    # drop planets with large H/R
    elif HR>2.e4:
      print('dropping a planet with high H/R',i,HR,Mp,data['name'][i])
      ###idrop.append(i)
      pass
    
    # add in a second check for bad HR (K2-22 b barely fails above check)
    # hmm, not sure what's going on.  just take out K2-22 b by hand, for now...
    #    elif HR>2.7e4*(data['mmw'][i]/2.35):
    #      print 'um special dropping a planet with high mmwH/R',i,HR,Mp,data['name'][i],data['mmw'][i]
    #      idrop.append(i)
    #    elif HR>1.8e4:
    #      print 'special dropping a planet with high mmwH/R',i,HR,Mp,data['name'][i],data['mmw'][i]
    #      idrop.append(i)

    elif g<0.1:
      print('dropping a planet with low gravity',i,g, \
        data['M_p'][i],data['R_p'][i],data['name'][i])
      ###idrop.append(i)
      pass
    
  for field in list(data.keys()):
    data[field] = np.array(data[field])
    data[field] = np.delete(data[field],idrop)
  nplanets = len(data['M_p'])
  print('nplanets',nplanets)

  for i in range(nplanets):  
    rho = 5.51*data['M_p'][i]/data['R_p'][i]**3
    if rho<0.5:
       print('low-density planet',i,rho,data['name'][i],data['M_p'][i],data['R_p'][i])

#_____SNR CUT (NO LONGER IMPLEMENTED)____

  SNRcut = 300. 
  emitFactor = 20.
  # lower the threshold, so as to get of order 500 known targets
  SNRcut = 140.

  # let's drop these thresholds for now
  emitFactor = 1.
  SNRcut = 0.

  goodStars = np.where(data['SNRfactor']>SNRcut)
  goodStarsEmission = np.where(data['SNRfactorEmission']>SNRcut/emitFactor)
  print('goodStars    ',len(goodStars[0]))
  print('goodStarsEmit',len(goodStarsEmission[0]))
  #allGoodStars = np.where((data['SNRfactor']>SNRcut) |
  #                      (data['SNRfactorEmission']>SNRcut/emitFactor))
  allGoodStars = np.where(data['SNRfactor']>SNRcut)
  print('all goodStars',len(allGoodStars[0]))

  for field in list(data.keys()):
    data[field] = np.array(data[field])
    data[field] = data[field][allGoodStars]

  print('# of planets',nplanets)
  nplanets = len(data['hmag'])
  print('# of planets',nplanets)

#_________________________SORTING________________________


# sort the data by some value, e.g. by GJ number
  i1 = []
  i2 = []
  for i in range(nplanets):
    i1.append(i)
    i2.append(i)
  print('# of planets to be sorted:',nplanets)
  for j in range(nplanets-2):
    for i in range(nplanets-1-j):
      if data['SNRfactor'][i1[i]] < \
             data['SNRfactor'][i1[i+1]]:
        iswap = i1[i]
        i1[i] = i1[i+1]
        i1[i+1] = iswap        
      if data['SNRfactorEmission'][i2[i]] < \
             data['SNRfactorEmission'][i2[i+1]]:
        iswap = i2[i]
        i2[i] = i2[i+1]
        i2[i+1] = iswap        
        
  for i in range(nplanets):
    # locate the data index for sort index 0,1,2,...
    # add 1, to convert from an index to a rank 
    data['trnsmit'][i] = i1.index(i)+1
    # flag non-transmission (emission) targets as rank = 6666
    # get rid of this 6666 stuff. just keep the crappy once anyway, with rank
    if 1:
      if data['SNRfactor'][i]<SNRcut:
        data['trnsmit'][i] = 6666

    data['emit'][i] = i2.index(i)+1
    # flag non-emission (transmission) targets as rank = 6666
    # get rid of this 6666 stuff. just keep the crappy once anyway, with rank
    if 1:
      if data['SNRfactorEmission'][i]<SNRcut/emitFactor:
        data['emit'][i] = 6666
    #  print 'trnsmit flags',data['trnsmit']


#_________________________OUTPUT_________________________
  
  dir = './'
  if icsv:
    filename = 'knownTargets.csv'
#    outfile = csv.writer(dir+filename)
    sep = ','
  else:
#    filename = 'realPlanets.txt'
    filename = 'knownTargets.txt' 
    sep = ' | '

  if ifakemasses:
    if 'realMp' not in desiredColumns:
      desiredColumns.insert(4,'realMp')

  outfile = open(dir+filename,'w')

  for field in desiredColumns:
    if field=='name':
      outfile.write(str('%12s' %field)+sep)
#    elif field=='Teff_p':
#      outfile.write(str('%7s' %('Teff'))+sep)
    else:
      outfile.write(str('%7s' %field)+sep)
  outfile.write('\n')

  for ii in range(nplanets):
#    i = ii
# use SNR-sorted indicing
    i = i1[ii]

#    print 'checking out planet:',ii,i,nplanets,data['name'][i]
    
    T = data['Teff_p'][i]
#    print 'R_p',data['R_p'][i]
    Rp = data['R_p'][i]*6.371e8/7.1492e9
    Mp = data['M_p'][i]*5.972e27/1.898e30
    mmw = data['mmw'][i]
    met = data['logMet'][i]
    g = Mp/Rp**2
#    print 'R T M g',T,Rp,Mp,g
#    print 'R T M g',T,'x'
    HR = T*Rp/Mp
# print out worst offenders for high H/R
# >2.e4 (2.78e4 analytically) completely fails.  >1.e4 might be useful
#    if HR>1.e4:
#      print 'H/R T Rp Mp',HR,T,Rp,Mp,'  ',mmw,met,'mmw met'

# drop planets with low Temperature.
#   400K removes 40; 320K removes 19 out of 128
# actually, better be more strict than 320, since inference needs elbow room
#    if T<400.:
#      print 'dropping a planet with low temperature',i,T
#      exit('shouldnt go here anymore')
# drop planets with large H/R.  this removes 2 out of 88
#    elif HR>2.e4:
#      print 'dropping a planet with high H/R',i,HR
#      exit('shouldnt go here anymore')

#    else:
    if 1:
      #print 'keeping this HR',i,data['name'][i],HR
#      print data.keys()
        
      for field in desiredColumns:
        if field:        
          #print 'field',field
          if data[field][i]=='missing':
            outfile.write(data[field][i]+sep)
          elif field=='name':
            outfile.write(str('%12s' %data[field][i])+sep)
          elif field=='Teff_p' or field=='Teff_*' or field=='dur1' or \
                   field=='trnsmit' or field=='emit' or field=='real' or \
                   field=='realMp':
#            print 'int field check',field,i,data[field][i]
            try:
              outfile.write(str('%7i' %data[field][i])+sep)
            except:   # (exception needed for NaNs)
              outfile.write(str('%7s' %data[field][i])+sep)
          else:
            if field=='Period_err' or field=='T_transit_err':
              outfile.write(str('%7.2e' %float(data[field][i]))+sep)
            elif field=='a_p' or field=='a_p_err':
              outfile.write(str('%7.4f' %float(data[field][i]))+sep)
            else:
              #print(i,data[field][i])
              outfile.write(str('%7.3f' %float(data[field][i]))+sep)
      outfile.write('\n')
  outfile.close()
