"""Author Ken Aoki 6/27 
performance of the rocket engine
Will calculate the thrust, and Isp
Thrust is the amount of force that the rocket engine will produce 
Isp is specific impulse and it is a measure of how efficient the rocket engine is 
"""
import math 
import scipy.constants as const 
from src.thermochemistry import get_propellant_properties
from src.nozzle import mach_from_area_ratio, exit_conditions, thrust_coefficient, throat_area, exit_area
import matplotlib.pyplot as plt
import numpy as np
def compute_thrust (mdot: float, v_exit: float, Pe: float, Pa: float, Ae: float) -> float: 
    """calculates the thrust provided by the rocket engine,
    the thrust provided by rocket engine comes from 2 things: 
    the momentum of the gas exiting the nozzle 
    the pressure difference at exit plane acting over area Ae
    F_momentum = mdot * velocity 
    F_pressure = (Pe - Pa)Ae 
    
    Args: 
    mdot: mass flow rate [kg/s]
    v_exit: velocity of gas exiting nozzle [m/s]
    Pe: pressure at nozzle exit [Pa]
    Pa: ambient pressure of atmosphere [Pa]
    Ae: area of exit [m^2]
    returns: 
    thrust [N]"""
    F_momentum = mdot * v_exit
    F_pressure = (Pe - Pa) * Ae 
    Force_thrust = F_momentum + F_pressure 
    return Force_thrust 

def specific_impulse (Force_thrust:float, mdot: float) -> float: 
    """calculates the specific impulse which measures the efficeincy of the rocket engine 
    specific impulse has units of seconds 
    it measures how many seconds a rocket engine can produce 1 N of thrust for consuming 1 N of propellant
    Isp = Force_thrust / (g0 * mdot)
    Arugs:
    Force_thrust [N]
    g0 gravity @ sea level [m/s^2]
    mdot mass flow rate [kg/s]"""
    g0 = 9.80665
    Isp = Force_thrust / (g0 * mdot)
    return Isp 

def compute_isp(propellant: str, OF:float, Pc:float, epsilon:float, Pa:float, mdot:float) -> float: 
    """calculates the isp as a function of only the Oxidiser and Fuel ratio OF
    props = get_propellant_properties
    """
    props = get_propellant_properties(propellant, OF)
    Tc = props['Tc']
    gamma = props['gamma']
    Mmol = props['Mmol']
    R_specific = 8.314 / Mmol 
    Me = mach_from_area_ratio(epsilon, gamma)
    Pe,Te,Ve = exit_conditions(Pc, Tc, gamma, Me, Mmol)
    Cf = thrust_coefficient(gamma, Pe, Pc, Pa , epsilon) 
    At = throat_area(1000, Cf, Pc)   # F_target = 1000 N
    Ae = exit_area(epsilon, At)
    F = compute_thrust(mdot,Ve,Pe,Pa,Ae)
    Isp = specific_impulse(F,mdot)
    return Isp 

def plot_isp_vs_of(Pc: float, epsilon: float, Pa: float, mdot: float):
    """plots Isp vs O/F ratio for all 3 propellant combinations
    Args:
    Pc: chamber pressure [Pa]
    epsilon: area ratio [-]
    Pa: ambient pressure [Pa]
    mdot: mass flow rate [kg/s]
    """
    propellants = {
        'lox_rp1':     np.arange(2.0, 3.75, 0.25),
        'lox_lh2':     np.arange(4.0, 7.5,  0.5),
        'n2o_ethanol': np.arange(3.5, 7.0,  0.5)
    }

    for propellant, of_range in propellants.items():
        isp_values = []
        for of in of_range:
            isp = compute_isp(propellant, of, Pc, epsilon, Pa, mdot)
            isp_values.append(isp)
        plt.plot(of_range, isp_values, label=propellant)

    plt.xlabel('O/F Ratio [-]')
    plt.ylabel('Isp [s]')
    plt.title('Isp vs O/F Ratio')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_thrust_vs_altitude(propellant, of_ratio, Pc, epsilon, mdot):
    props = get_propellant_properties(propellant, of_ratio)
    Tc = props['Tc']
    Mmol = props['Mmol']
    gamma = props['gamma']
    Me = mach_from_area_ratio(epsilon, gamma)
    Pe, Te, Ve = exit_conditions(Pc, Tc, gamma, Me, Mmol)
    Pa_sea = 101325
    Cf = thrust_coefficient(gamma, Pe, Pc, Pa_sea, epsilon)
    At = throat_area(1000, Cf, Pc)
    Ae = exit_area(epsilon, At)
    altitudes = np.arange(0,80000,1000)
    thrust_values = []

    for alt in altitudes:
        Pa = 101325 * math.exp(-alt / 8500)
        F = compute_thrust(mdot, Ve, Pe, Pa, Ae)
        thrust_values.append(F)
            
    plt.plot(altitudes, thrust_values , label = propellant)
    plt.xlabel('Altitude [meters]')
    plt.ylabel('Thrust [Newtons]')
    plt.title('Altitude vs Thrust')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_thrust_vs_mdot(propellant, of_ratio, Pc, epsilon, mdot): 
    props = get_propellant_properties(propellant,of_ratio)
    Pa = 101325
    Tc = props['Tc']
    Mmol = props['Mmol']
    gamma = props['gamma']
    mdot_values = np.arange(0,50,1)
    Me = mach_from_area_ratio(epsilon, gamma)
    Pe,Te,Ve = exit_conditions(Pc, Tc, gamma, Me, Mmol)
    Cf = thrust_coefficient(gamma, Pe, Pc,Pa,epsilon)
    At = throat_area(1000, Cf, Pc)
    Ae = exit_area(epsilon, At)

    Thrust_values = []
    for mdot in mdot_values: 
        F = compute_thrust(mdot, Ve, Pe, Pa, Ae)
        Thrust_values.append(F)
    plt.plot(mdot_values, Thrust_values , label = propellant)
    plt.xlabel('Mass Flow Rate [kg/s]')
    plt.ylabel('Thrust [N]')
    plt.title('Thrust vs Mass Flow Rate')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    plot_isp_vs_of(Pc=3.45e6, epsilon=10, Pa=101325, mdot=10)
    plot_thrust_vs_altitude('lox_rp1', 2.75, 3.45e6, 10, 10)
    plot_thrust_vs_mdot('lox_rp1', 2.75, 3.45e6, 10, 10)

