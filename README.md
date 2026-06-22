<<<<<<< HEAD
# LRE_Sizing_Tool Python software tool that designs a liquid rocket engine from first principles: you give it a propellant combination and target thrust, and it works through the full engine sizing chain pulling combustion properties (temperature, specific heat ratio, molecular weight) from tabulated NASA CEA data, sizing the combustion chamber using the characteristic length L* method, solving the isentropic flow relations to determine throat and exit geometry, computing thrust and specific impulse, estimating wall heat flux via the Bartz equation, and generating performance curves across mixture ratio and altitude, validated against CEA within ±5%
=======
# LRE_Sizing_Tool





thermochemistry.py
gets cea data and interpolates Temperature, gamma, and Mmol 

chamber.py 
calculate c* value (Tc, gamma, Mmol) -> c* [m/s]
calculate the chamber dimensions (c*, mdot, Pc, L*) -> volume, L, D [m^3, m, m]

nozzle.py
calculate the throat area (F, Pc, Cf) -> At [m^2]
calculate the exit area (At, area_ratio) -> Ae [m^2]
calculate the exit conditions (Pc, gamma, Me) -> Ve, Pe, Te

performace.py
calculate the thrust  (mdot, Ve, Pe, Pa, Ae) → F 
calculate the Isp (F, mdot) → Isp
>>>>>>> 33fe49a36e0a94e28593a66447e74fbe51a5a9ba
