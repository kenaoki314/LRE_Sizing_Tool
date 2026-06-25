"""
test_thermochemistry.py

Validates that get_combustion_properties() returns correct values for
LOX/RP-1 by comparing against the source CEA table at known O/F points.

Tolerance: exact match at table nodes 
"""

import pytest
from src.thermochemistry import get_propellant_properties

LOX_RP1_TABLE = [
    (2.00, 3284.9177, 1.1827, 20.7375),
    (2.25, 3466.1841, 1.1761, 21.9373),
    (2.50, 3552.2443, 1.1816, 22.9241),
    (2.75, 3586.1270, 1.1877, 23.7541),
    (3.00, 3593.2163, 1.1908, 24.4723),
    (3.25, 3585.9737, 1.1911, 25.1068),
    (3.50, 3570.5588, 1.1896, 25.6748),
]


# pytest.mark.parametrize runs this test once per row in LOX_RP1_TABLE.
# The variable names on the left match the tuple positions on the right.
@pytest.mark.parametrize("of, Tc_ref, gamma_ref, Mmol_ref", LOX_RP1_TABLE)
def test_loxrp1_table_nodes(of, Tc_ref, gamma_ref, Mmol_ref):
    """At table nodes, interpolation must return exact CEA values."""
    props = get_propellant_properties(of_ratio=of, propellant="lox_rp1")

    # abs=0.01 means tolerance of 0.01 K on Tc — tight, as expected at a node
    assert props["Tc"]    == pytest.approx(Tc_ref,    abs=0.01),  f"Tc mismatch at O/F={of}"
    assert props["gamma"] == pytest.approx(gamma_ref, abs=0.0001), f"gamma mismatch at O/F={of}"
    assert props["Mmol"]  == pytest.approx(Mmol_ref / 1000,  abs=0.000001),  f"Mmol mismatch at O/F={of}"


def test_extrapolation_blocked_low():
    """Query below O/F range must raise ValueError."""
    with pytest.raises(ValueError):
        get_propellant_properties(of_ratio=1.5, propellant="lox_rp1")


def test_extrapolation_blocked_high():
    """Query above O/F range must raise ValueError."""
    with pytest.raises(ValueError):
        get_propellant_properties(of_ratio=4.0, propellant="lox_rp1")

# --- LOX/LH2 table nodes ---
LOX_LH2_TABLE = [
    (4.0, 2921.5899, 1.1878,  9.9789),
    (4.5, 3094.3721, 1.1755, 10.8893),
    (5.0, 3229.5660, 1.1688, 11.7573),
    (5.5, 3331.7752, 1.1670, 12.5796),
    (6.0, 3405.1552, 1.1690, 13.3541),
    (6.5, 3453.8322, 1.1731, 14.0792),
    (7.0, 3482.1468, 1.1771, 14.7552),
]

@pytest.mark.parametrize("of, Tc_ref, gamma_ref, Mmol_ref", LOX_LH2_TABLE)
def test_loxlh2_table_nodes(of, Tc_ref, gamma_ref, Mmol_ref):
    """At table nodes, interpolation must return exact CEA values."""
    props = get_propellant_properties(of_ratio=of, propellant="lox_lh2")
    assert props["Tc"]    == pytest.approx(Tc_ref,    abs=0.01)
    assert props["gamma"] == pytest.approx(gamma_ref, abs=0.0001)
    assert props["Mmol"]  == pytest.approx(Mmol_ref / 1000,  abs=0.000001)


# --- N2O/Ethanol table nodes ---
N2O_ETHANOL_TABLE = [
    (3.5, 2790.3161, 1.2112, 23.8311),
    (4.0, 2967.9068, 1.1862, 24.8302),
    (4.5, 3065.6945, 1.1694, 25.6021),
    (5.0, 3103.3217, 1.1631, 26.1816),
    (5.5, 3106.4202, 1.1614, 26.6430),
    (6.0, 3091.4573, 1.1611, 26.9730),
    (6.5, 3066.9443, 1.1616, 27.2545),
]

@pytest.mark.parametrize("of, Tc_ref, gamma_ref, Mmol_ref", N2O_ETHANOL_TABLE)
def test_n2o_ethanol_table_nodes(of, Tc_ref, gamma_ref, Mmol_ref):
    """At table nodes, interpolation must return exact CEA values."""
    props = get_propellant_properties(of_ratio=of, propellant="n2o_ethanol")
    assert props["Tc"]    == pytest.approx(Tc_ref,    abs=0.01)
    assert props["gamma"] == pytest.approx(gamma_ref, abs=0.0001)
    assert props["Mmol"]  == pytest.approx(Mmol_ref / 1000,  abs=0.000001)