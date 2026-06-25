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

L* tells us the length the chamber must be to give the propellant ample time to fully vaporize, atomize, mix and react. 
L* is the ratio of the Volumme of the chamber Vc to the area of the throat nozzle A*
L* = V_c / A* 
Vc = L* * A* 
V_c m^3 
A* m^2
L* gives us V_c from A* and constrains how much volume we need
V_c and L/D choice constrains what geometry achieves this volume
LOX / RP-1 = 1.143m 
LOX / LH2 = 0.635m
N2O / Ethanol = 1.65
Supported propellant combinations:
    - lox_rp1  : LOX (90 K) / RP-1 (293 K), Pc = 3.45 MPa, shifting equilibrium
    - lox_lh2 : LOX (90K) / H(20K), Pc=3.45 MPa, shifting equilibrium. 
    - n2o_ethanol: N2O (293K) / C2H5OH Ethanol (293K) Pc = 3.45 Mpa, Shfitig equilibum 

Author Ken Aoki, 10:12PM 6/23/2026 """

import math
from src.thermochemistry import get_propellant_properties



def gamma_Func(gamma:float)-> float :
    """turns gamma into Vandenkerchove function
    gamma unitless
    gamma function uniltess """
    #gamma = 1.67 ####PLACE HOLDER FOR CALCULATED gamma VALUE FROM thermochemistry.py
    
    VDK_function = math.sqrt(gamma) * (2/(gamma +1))**((gamma+1)/(2*(gamma-1)))
    return  VDK_function


def cstar(VDK_function:float, R: float, Tc:float) -> float: 
    """calculates C star as a function of Vandenkerchove function, Chamber Temperature, and R specific gas constant
    with R_specific = R_universal / M_mol
   returns: C* [m/s
    R J/kg*K
    Tc K]"""
    Vandenkerckhove = VDK_function 
    #R = 8.314/0.01118  # [ J / (mol*K) ] ###PLACE HOLDER FOR CALCULATED Mmol VALUE FROM thermochemistry.py
    #Tc = 3140.3 K
    Cstar = math.sqrt(R * Tc) / Vandenkerckhove
    return Cstar

Lstar_Values = {
    'lox_rp1': 1.143,
    'lox_lh2': 0.635,
    'n2o_ethanol': 1.65}
def chamberVolume(A_throat: float, propellant: str) -> float: 
    """look up Lstar value and plug and chug for solkving for chamber volume
    A_throat = area of throat [m^2]
    Chamber Volume = volume of chamber [m^3]
    Lstar characteristic length of the chamber"""
    Lstar = Lstar_Values.get(propellant)
    if Lstar is None: 
        raise ValueError(f'Propellant {propellant} not found')
    
    Chamber_Vol = A_throat * Lstar #placeholder for A_throat after it is calculated 
    return Chamber_Vol

def chamber_dimensions(Chamber_vol: float, LD_ratio: float) -> dict: 
    """get chamber dimesnions from a L/D ratio and the Volume of Chamber 
    L_c is the length of the chamber
    D_c is the diamter of the chamber
    V_c = pi/4 * D_c^2 * L_c
    D_c = (4 · V_c / (π · (L/D)))^(1/3)
    L_c = (L/D)*D_c"""
    Chamber_Diameter = ((4 * Chamber_vol) / (math.pi * LD_ratio))**(1/3)    
    Chamber_Length = LD_ratio * Chamber_Diameter
    return {'L_c': Chamber_Length, 'D_c':Chamber_Diameter}








if __name__ == '__main__':
    Propellant = 'n2o_ethanol'
    OF_ratio = 5.7
    props = get_propellant_properties(Propellant , OF_ratio)
    Tc = props['Tc']
    gamma = props['gamma']
    Mmol = props['Mmol']
    R_universal = 8.314
    R_specific = R_universal / Mmol
    gamma_func_result = gamma_Func(gamma)
    cstar_result = cstar(gamma_func_result, R_specific, Tc)
    print(f'for {Propellant} with OF ratio {OF_ratio}, characteristic velocity c* is: {cstar_result} m/s')
    A_throat_placeholder = 0.01  # m^2 — placeholder until nozzle.py is complete
    chamber_vol = chamberVolume(A_throat_placeholder, Propellant)
    dims = chamber_dimensions(chamber_vol, LD_ratio=2.0)
    print(f"Chamber Volume: {chamber_vol:.6f} m^3")
    print(f"Chamber Diameter: {dims['D_c']:.4f} m")
    print(f"Chamber Length: {dims['L_c']:.4f} m")