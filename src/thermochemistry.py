"""
thermochemistry.py

Provides combustion property lookups (Tc, gamma, Mmol) as a function of
O/F ratio by linear interpolation from tabulated NASA CEA data.



Supported propellant combinations:
    - lox_rp1  : LOX (90 K) / RP-1 (293 K), Pc = 3.45 MPa, shifting equilibrium
    - lox_lh2 : LOX (90K) / H(20K), Pc=3.45 MPa, shifting equilibrium. 
    - n2o_ethanol: N2O (293K) / C2H5OH Ethanol (293K) Pc = 3.45 Mpa, Shifting equilibrium 

Author : Ken Aoki 6/21/26
Project: LRE Sizing Tool — Phase 1 
"""

import numpy as np
import pandas as pd 
from pathlib import Path 

def get_propellant_properties(propellant:str, of_ratio: float) -> dict:
    """Interpolates properties from CEA .csv file data 
    Arguments:
    propellant: str 
    of_ratio: float 
    
    returns:
    Tc chamber temperature [K]
    gamma ratio of specific heats none
    Mmol molar mass [kg/mol]
    raises key error if propellant string is not recognized
    fileNotFoundError if CSV is missing data
    ValueError if outside OF data range"""
    propellant_files = {
        'lox_rp1': 'cea_loxrp1.csv',
        'lox_lh2': 'cea_loxlh2.csv',
        'n2o_ethanol': 'cea_n2o_ethanol.csv'    
        }
    if propellant not in propellant_files: 
        raise KeyError(f"unknown propellant'{propellant}'."
        f"Choose from: {list(propellant_files.keys())}")
    
    filename = propellant_files[propellant]
    filepath = Path(__file__).parent.parent/ 'data' / filename
    df = pd.read_csv(filepath)  
    OF = df['of_ratio'].to_numpy()
    Tc = df['Tc_K'].to_numpy()
    gamma = df['gamma'].to_numpy()
    Mmol = df['Mmol_kg_kmol'].to_numpy() / 1000.0 #converting kg/kmol to kg/mol
    if not (OF[0] <= of_ratio <= OF[-1]):
        raise ValueError(
            f"of_ratio={of_ratio} is outside tabulated range "
            f"[{OF[0]}, {OF[-1]}] for propellant '{propellant}'"
        )
    Tc_value = np.interp(of_ratio, OF, Tc)
    gamma_value = np.interp(of_ratio, OF, gamma)
    Mmol_value = np.interp(of_ratio, OF, Mmol)
    return {'Tc': Tc_value, 'gamma': gamma_value, 'Mmol': Mmol_value}
if __name__ == "__main__":
    propellant = 'lox_rp1'
    OF_ratio = 3.5
    result = get_propellant_properties(propellant, OF_ratio )
    print(f'For {propellant} with O/F ratio {OF_ratio}')
    print(f"Tc = {result['Tc']:.1f} K")
    print(f"gamma = {result['gamma']:.4f}")
    print(f"Mmol  = {result['Mmol']:.5f} kg/mol")