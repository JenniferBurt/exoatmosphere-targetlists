import numpy as np
#from thermo import thermo
from thermo import *

#_________________________________________________________________________

def calcMMW(Tiso,logMet,logCtoO,Rp,Rstar,logg):
    
    Met=10.**logMet
    CtoO=10.**logCtoO
# g0 isn't actually used anywhere. ?
#    g0=(10.**logg)/100. #from logg in cgs to m/s2
   
    #Setting up atmosphere grid
#    logP = np.arange(-7,1.5,0.08)+0.08
# logP had length 107. now it's length 1.  should speed things up.
#    print logP
#    print len(logP)#
#    logP = np.arange(-3,1.5,0.5)+0.5  
#    logP = np.arange(-3,-1.5,0.5)+0.5
    logP = np.array([-3])  
#    logP = np.array([-3])  # T=185K, logMet=1.6 still hits this one
#    logP = np.array([-5])  # T=280K, logMet=1.1 still hits this one Rp=0.3,Rstar=0.66
#    logP = np.array([-6]) # dang it. T=539K, 0.223,0.89, met=2.29,-0.18
#    logP = np.array([1])
#    print logP
    P = 10.0**logP
    T = np.zeros(len(P))+Tiso 
  
    #making courser chemistry grid
#    Pchem=np.append(P[::8],P[-1])
#    Tchem=np.append(T[::8],T[-1])
# redo Pchem,Tchem (otherwise they're length of 2 with same value)
    Pchem=P
    Tchem=T
#    print 'Pchem',Pchem,Tchem
#    print 'thermo inputs',Met, CtoO, Tchem, Pchem
    H2Oarr, CH4arr, COarr, CO2arr, NH3arr, N2arr, HCNarr, H2Sarr, PH3arr, \
            C2H2arr, C2H6arr, Naarr, Karr, TiOarr, VOarr, \
            FeHarr, Harr, H2arr, Hearr, \
            MMWarr = \
            thermo(Met, CtoO, Tchem, Pchem,'foobee')

#    print 'thermo results1',H2Oarr, CH4arr, COarr, CO2arr
#    print 'thermo results2',NH3arr, N2arr, HCNarr, H2Sarr, PH3arr
#    print 'thermo results3',C2H2arr, C2H6arr, Naarr, Karr
#    print 'thermo results4',TiOarr, VOarr,FeHarr
#    print 'thermo results5',Harr, H2arr, Hearr
#
#    print 'thermo results H2',H2arr
#    print 'thermo results He',Hearr

    #interoplating back to full grid
    H2Oarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(H2Oarr))
    CH4arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(CH4arr))*1.
    COarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(COarr))*1.
    CO2arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(CO2arr))*1.
    NH3arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(NH3arr))*1.
    N2arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(N2arr))*1.
    HCNarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(HCNarr))*1.
    H2Sarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(H2Sarr))*1.
    PH3arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(PH3arr))*1.
    C2H2arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(C2H2arr))*1.
    C2H6arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(C2H6arr))*1.
    Naarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(Naarr))*1.
    Karr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(Karr))*1.
    TiOarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(TiOarr))*1.
    VOarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(VOarr))*1.
    FeHarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(FeHarr))*1.E-14
    Harr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(Harr))
    H2arr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(H2arr))
    Hearr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(Hearr))
    MMWarr = 10.**interp(np.log10(P),np.log10(Pchem),np.log10(MMWarr))
    
    mmw = 2.*H2arr + 4.*Hearr+18.*H2Oarr+16*CH4arr+28.*COarr+44.*CO2arr+17.*NH3arr+34.*H2Sarr+28.*N2arr+1.*Harr+63.9*TiOarr+66.94*VOarr+23.*Naarr+39.1*Karr+56.8*FeHarr+26.04*C2H2arr+27.03*HCNarr

# use the CEA mean molecular weight, rather than the above sum
    if len(mmw)!=len(MMWarr):
        exit('array size problem with MMW in fm.py')
    mmw=MMWarr

    mmw[mmw<2.35]=2.35  #in case errors in chemistry

    return mmw
