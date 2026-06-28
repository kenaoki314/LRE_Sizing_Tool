"""tests for nozzle.py"""

import pytest
import math
from src.nozzle import mach_from_area_ratio,temperature_exit,pressure_exit,velocity_exit,exit_conditions , nozzle_geometry


def test_mach_from_area_ratio():
    result = mach_from_area_ratio(10, 1.1877)
    assert result == pytest.approx(3.243, rel=0.01)

def test_exit_conditions_temperature():
    result = temperature_exit(1.1877, 3586, 3.243)
    assert result == pytest.approx(1805, rel=0.02)

def test_exit_conditions_velocity():
    R_specific = 8.314 / 0.02375
    result = velocity_exit(3.243, 1.1877, R_specific, 1805)
    assert result == pytest.approx(2809, rel=0.02)

def test_nozzle_geometry_lengths(): 
    result = nozzle_geometry(math.pi * 0.05**2,math.pi * 0.15**2,math.pi * 0.10**2)
    assert result['L_conv'] == pytest.approx(0.1732, rel=0.01)
    assert result ['L_div'] == pytest.approx(0.1867, rel=0.01)
    assert result ['Rt'] == pytest.approx(0.05, abs=1e-6)
    assert result ['Re'] == pytest.approx(0.10, abs=1e-6) 
    assert result ['Rc'] == pytest.approx(0.15, abs=1e-6)

def test_nozzle_geometry_defaults():
    result = nozzle_geometry(math.pi * 0.05**2,math.pi * 0.15**2,math.pi * 0.10**2)
    assert result['L_conv'] == pytest.approx(0.1732, rel=0.01)
    assert result['L_div'] == pytest.approx(0.1867, rel=0.01)