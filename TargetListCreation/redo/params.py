def Parameters():

  params={
    'outputColumns':
       ['name',        
        'real','realMp',
        'RA','Dec',
        'M_*','R_*','R_*_err','Teff_*','Teff_*_err','logg_*',
        #'M_p','R_p','R_p_err','Teff_p','logg',
        'M_p','M_p_err','R_p','R_p_err','Teff_p','logg',
        'mmw0','mmw',
        'logMet0','logMet','logMet_*',
        'logCtoO','logCtoO_*',
        #'hmag','distance','dur1','a_p','a_p_err','Period',
        'hmag','jmag','vmag','distance','dur1','a_p','a_p_err','Period','Period_err',
        # new 11/11/21 (plus the two new error bars above)
        'T_transit','T_transit_err',
        'ecc', 'ecc_err', 'omega', 'omega_err',
        'SNRfactor','SNRfactorEmission',
        'Pc','hazeSlope','hazeAmp','spectral modulation', 'spectral modulation [ppm]'
       ],

    'confirmedDataFile':'confirmedPlanets.csv', # file with confirmed planets from the NASA Exoplanet Archive
    'confirmedDataFields':
         ['pl_hostname','pl_name','pl_letter','pl_discmethod',
          'ra','dec',
          'pl_massj','pl_msinij','pl_radj',
          'pl_masse','pl_msinie','pl_rade',
          'pl_masselim','pl_msinielim',
          'pl_orbper','pl_orbsmax','pl_orbeccen','pl_orbincl',
          'st_lum','st_mass','st_rad','st_teff',
          'pl_tranflag','pl_astflag','pl_rvflag','pl_imgflag',
          'pl_eqt','pl_insol',
# more new ones (for RobZ)
          'st_tefferr1','st_tefferr2',
          'st_raderr1','st_raderr2',
          'pl_radeerr1','pl_radeerr2',
          'pl_orbsmaxerr1','pl_orbsmaxerr2',
          'pl_orblper', 'pl_orblpererr1', 'pl_orblpererr2',
          'pl_orbeccenerr1', 'pl_orbeccenerr2',
#          'pl_orbpererr1','pl_orbpererr2',
# new ones:
          'st_dist',
          'pl_trandur','st_metfe','st_h'],

    # NEW FIELDS FOR PSCOMPPARS TABLE
    # DROP: pl_letter (no actually it's there in default download;
    #                  maybe not on default save-download file though)
    #   'pl_msinij','pl_msinie','pl_msinielim',
    # RENAMED: pl_hostname pl_discmethod  mass-->bmass
    #   st_dist st_metfe st_h-->sy_hmag
    #   'pl_tranflag','pl_astflag','pl_rvflag','pl_imgflag',
    #     actually 'img_flag' doesnt exist
    'confirmedDataFields':
         ['hostname','pl_name','pl_letter','discoverymethod',
          'ra','dec',
          'pl_radj','pl_rade',
          'pl_bmassj','pl_bmasse','pl_bmasselim',
          'pl_bmasseerr1','pl_bmasseerr2',
          'pl_orbper','pl_orbsmax','pl_orbeccen','pl_orbincl',
          'pl_orbpererr1','pl_orbpererr2',
          'pl_tranmid','pl_tranmiderr1','pl_tranmiderr2',
          'st_lum','st_mass','st_rad','st_teff',
          'pl_eqt','pl_insol',
          'tran_flag','ast_flag','rv_flag',
          'st_tefferr1','st_tefferr2',
          'st_raderr1','st_raderr2',
          'pl_radeerr1','pl_radeerr2',
          'pl_orbsmaxerr1','pl_orbsmaxerr2',
          'pl_orblper', 'pl_orblpererr1', 'pl_orblpererr2',
          'pl_orbeccenerr1', 'pl_orbeccenerr2',
          'sy_dist',
          'pl_trandur','st_met','sy_hmag','sy_jmag','sy_vmag',
          'pl_orblper', 'pl_orblpererr1', 'pl_orblpererr2'
         ],

    'keplerDataFile':'keplerPlanets.csv',       # file with Kepler planets from the NASA Exoplanet Archive
    'keplerDataFields':
        ['kepid','kepler_name','koi_disposition',
         'ra','dec',
         'koi_prad',             
         'koi_period','koi_sma','koi_eccen','koi_incl',
         'koi_teq','koi_insol'],
    'archiveDir':'archiveData',                 # directory where these two files are located 
      
    'onlyConfirmed':True,   # only plot confirmed planets

    'plotPhaseSpace':True,  # plot the overall planet phase space
    'plotMassRadius':True, # plot the function used to convert R to M

    'modelColor':'red',     # color for plots of model data
    'rvColor':'orange',     # color for RV-detected planet 
    'transitColor':'purple',# color for transit-detected planet 
    'otherColor':'black',   # color for other-detected planet 
    'pointSize':5           # size of plot points
    }

  return params

