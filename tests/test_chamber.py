"""tests chamber.py to validate that we achieve
correct gamma function 
cstar
chamber volume
chamber dimesnions
chamber volume raise bad propellant error """



import pytest
import math
from src.chamber import gamma_Func, cstar, chamberVolume , chamber_dimensions

def test_gamma_func_known_value():
    """At gamma=1.4, Vandenkerckhove function = 0.6847"""
    result = gamma_Func(1.4)
    assert result == pytest.approx(0.6847, abs=0.0001)

def  test_cstar_known_value():
    """test cstar c* = 1459 m/s for gamma 1.4 Tc 3000K Mmol 0.025 kg/mol"""
    R_specific = 8.314 / 0.025
    vdk = gamma_Func(1.4)
    result = cstar(vdk, R_specific, 3000.0)
    assert result == pytest.approx(1459.0, abs=1.0)

def test_chamber_volume():
    "test at volume with placeholder A* until nozzle.py is complete, and loxrp1"
    result = chamberVolume(0.05, 'lox_rp1')
    assert result == pytest.approx(0.05715, abs=0.0001)

def test_chamber_dimensions():
    "test 1000 m^3 volume and 2.5 LD ratio"
    result = chamber_dimensions(1000, 2.5)
    assert result['D_c'] == pytest.approx(7.986, abs=0.001)
    assert result['L_c'] == pytest.approx(19.965, abs=0.001)  


def test_chamber_volume_bad_propellant():
    "will raise error"
    with pytest.raises(ValueError):
        chamberVolume(0.05, 'bad_propellant')