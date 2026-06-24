"""calculate c* value from values of Tc, gamma, and Mmol,
this is done by the equation c* = sqrt(R*T)/GammaFuntion
where R is the specific gas constant R = R_universal / M_mol 
M_mol is molecular weight 
T_c is the temperature at the chamber
Vandenkerckhove function(Gamma Function) represents compressibillity effect of gas as it accelerates to speed of sound at choke
Gamma function = sqrt(gamma)*[2/(gamma + 1))]exp((gamma+1)/2(gamma -1))
gamma is specific heat ratio c_p / c_v
c_p is specifc heat capacity at constant pressure 
c_v is specific heat capacity at constant volume

Author Ken Aoki, 10:12PM 6/23/2026 """

import math


def GammaFunc(gamma:float)-> float :
    """turns gamma into Vandenkerchove function"""
    gamma = 1.13 ####PLACE HOLDER FOR CALCULATED gamma VALUE FROM thermochemistry.py
    VDK_function = math.sqrt(gamma) * (2/(gamma +1))**((gamma+1)/(2*(gamma-1)))
    return {'GammaFunction': VDK_function }
Gamma = GammaFunc(1.17)

def Cstar(Gamma:float, R: float, Tc:float) -> float: 
    """calculates C star as a function of Vandenkerchove function, Chamber Temperature, and R specific gas constant
    with R_specific = R_universal / M_mol"""
    Vandenkerckhove = Gamma 
    R = 8.314/0.01118  # [ J / (mol*K) ] ###PLACE HOLDER FOR CALCULATED Mmol VALUE FROM thermochemistry.py
    Tc = 3140.3
    Cstar = math.sqrt(R * Tc) / Vandenkerckhove
    return {'Cstar':Cstar}
