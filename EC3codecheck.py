#-------------------------------------------------------------------------------
# Name:        EC3CodeChecks.py
# Purpose:     It contains main equations for EC3 code Checks
#
# Author:      cpicard
#
# Created:     01/08/2018;
# Modified:    
#               
# Copyright:   2018 Charles Picard
# Licence:     MIT
#-------------------------------------------------------------------------------
import numpy as np
import pandas as pd
   

def execute(mbr):
    cc = np.array([['','clause','UR','check']])
    def cc_append(cc,i,clause,mbr,fun):
        cdchk,UR = fun(mbr)
        cc  = np.append(cc,[[i,clause, UR, cdchk]],axis = 0)
        return cc
    
    #slowly append codechecks to the structure
    cc = cc_append(cc,1,'EQ (6.1)',mbr,EQ_6_1)
    cc = cc_append(cc,2,'EQ (6.2)',mbr,EQ_6_2)
    cc = cc_append(cc,3,'EQ (6.5)',mbr,EQ_6_5)
    cc = cc_append(cc,4,'EQ (6.9)',mbr,EQ_6_9)
    cc = cc_append(cc,5,'EQ (6.17)',mbr,EQ_6_17)
    cc = cc_append(cc,6,'EQ (6.19)',mbr,EQ_6_19)
    
    # convert to dataframe for easy sorting later
    cc_pd = pd.DataFrame(data = cc[1:,1:],
                         index = cc[1:,0],
                         columns = cc[0,1:])
    return cc_pd
    

class Member:
    def __init__(self):
        self.sxEd = np.zeros(1)
        self.szEd = np.zeros(1)
        self.tauEd = np.zeros(1)
        self.fy = np.zeros(1)
        self.gm0 = np.zeros(1)
        
    def Execute(self):
        self.codecheck = execute(self)
        return self.codecheck
    

def EQ_6_1(mbr):
    """
    INPUT:
        gM0     partial factor for resistance of cross-sections whatever the class is
        gM1     partial factor for resistance of members to instability assessed by member checks
        gM2     partial factor for resistance of cross-sections in tension to fracture
        sxEd    design value of the local longitudinal stress
        szEd    design value of the local transverse stress 
        tauEd   design value of the local shear stress 
        
    """
    sxEd  = mbr.sxEd
    szEd  = mbr.szEd
    tauEd = mbr.tauEd
    gM0   = mbr.gM0
    fy    = mbr.fy
    
    UR = (sxEd/fy/gM0)**2 + (szEd/fy/gM0)**2 - (sxEd/fy/gM0)*(szEd/fy/gM0)+ 3*(tauEd/fy/gM0)**2
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR)
    
    
def EQ_6_2(mbr):
    """
    INPUT:       
    """
    NEd   = mbr.NEd
    NRd   = mbr.NRd    
    MyEd  = mbr.MyEd
    MyRd  = mbr.MyRd    
    MzEd  = mbr.MzEd
    MzRd  = mbr.MzRd    

    UR = (NEd/NRd) + (MyEd/MyRd) + (MzEd/MzRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR)

def EQ_6_5(mbr):
    """
    INPUT:       
    """
    NEd  = mbr.NEd
    NtRd = mbr.NtRd
    gM0  = mbr.gM0
    gM2  = mbr.gM2
    A    = mbr.A
    Anet = mbr.Anet
    fy   = mbr.fy
    fu   = mbr.fy
    
    if Anet<A:
        NplRd = A*fy/gM0
        NuRd = 0.9*Anet*fu/gM2
        NtRd = np.min((NplRd,NuRd))
        
    UR = (NEd/NtRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR)        

def EQ_6_9(mbr):
    """
    DESC:       
    """
    NEd  = mbr.NEd
    NcRd = mbr.NcRd
    gM0  = mbr.gM0
    A    = mbr.A
    Aeff = mbr.Aeff
    fy   = mbr.fy
    cs_class = mbr.cs_class
    
    NcRd = A * fy /gM0
    
    if cs_class == 4:
        NcRd = Aeff* fy /gM0
        
    UR = (NEd/NcRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR) 


def EQ_6_12(mbr):
    """
    DESC:       
    """
    MEd  = mbr.MEd
    
    gM0  = mbr.gM0
    fy   = mbr.fy
    
    Wpl = mbr.Wpl
    Welmin = mbr.Welmin
    Weffmin = mbr.Weffmin
    cs_class = mbr.cs_class
    
    McRd = Wpl* fy /gM0
    
    if cs_class == 3:
        McRd = Welmin* fy /gM0
    if cs_class == 4:
        McRd = Weffmin* fy /gM0

                
    UR = (MEd/McRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR) 

def EQ_6_17(mbr):
    """
    DESC:       
    """
    VEd  = mbr.VEd
    gM0  = mbr.gM0
    fy   = mbr.fy
    Av   = mbr.Av
    VcRd = Av * fy / np.sqrt(3) / gM0   
    UR   = (VEd/VcRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR)

def EQ_6_19(mbr):
    """
    DESC:       
    """
    TEd  = mbr.TEd
    TRd = mbr.TRd   

    UR   = (TEd/TRd)
    
    cdchk = np.abs(UR)<1
    return cdchk,np.abs(UR)

def main():
    mbr = Member
    # INPUT #
    mbr.fy  = 355.
    mbr.fu  = 800.
    mbr.gM0 = 1.15
    mbr.gM1 = 1.15
    mbr.gM2 = 1.15
    
    # Stresses Example
    mbr.sxEd  = mbr.fy*np.random.random()
    mbr.szEd  = mbr.fy*np.random.random()
    mbr.tauEd = mbr.fy*np.random.random()
    # Forces
    mbr.NEd   = np.random.random()
    mbr.VEd   = np.random.random()
    mbr.MzEd  = np.random.random() 
    mbr.MyEd  = np.random.random()
    
    # CAPACITY  - Section Properties
    mbr.MyRd = 1  
    mbr.NRd  = 1    
    mbr.NtRd = 1
    mbr.NcRd = 1
    mbr.MzRd = 1
    
    mbr.A = 1
    mbr.Anet = 1
    mbr.Aeff = np.random.random()
    mbr.Av = np.random.random()
    mbr.cs_class = np.random.randint(1,4)
            
    cc_01 = mbr.Execute(mbr)
    print(cc_01)
    print("MAX",cc_01.loc[cc_01['UR'].idxmax()])
    return cc_01
    
if __name__ == '__main__':
    cc_main = main()