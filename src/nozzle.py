"""calculator to calculate the value of the throat area as a function of the force, pressure, and thrust coeeficient 

this will implement isentropic flow relatinos and solve mach area equation numerically
then it will calculate the value of the throar area as a function of the force, pressure, and the thrust coefficent 
then it will calculate the exit area A_e from area ratio by Pe/Pc or exit mach 
then output nozzle geometry and then calcualte exit velocity


Isp: specific impulse [s]
mdot: mass flow rate [kg/s]
g0: gravitational acceleration at sea level [m/s^2]
F: thrust [N]
C_f: thurst coefficient [none]
gamma: heat capacity ratio [none]
M: Mach number 

exhaust velocity c = Isp *g0 = F / mdot [m/s]
Throat area Ac = F / (C_f * P_c) [m^2]

Diverging bell curve:
A / A_t = 1/M * [(2+(gamma-1)M^2) / (gamma + 1)]^((gamma+1)/2(gamma-1))

P_exit = P_c * (1+ (gamma -1)/2 * M_exit^2)^(-gamma / (gamma -1))
T_exit = T_c * (1+(gamma-1)/2 * M_exit^2)^-1
V_exit
""" 

print("hello world")
