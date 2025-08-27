# app/fluid/fluid_props.py
"""
Simple fluid property helpers using CoolProp.
Returns density, dynamic viscosity, kinematic viscosity at P,T or for standard fluids.
"""

from CoolProp.CoolProp import PropsSI

def properties_PT(fluid, P, T):
    """
    fluid: string (CoolProp name)
    P: pressure [Pa]
    T: temperature [K]
    returns dict: rho [kg/m3], mu [Pa.s], nu [m2/s]
    """
    rho = PropsSI("D", "P", P, "T", T, fluid)
    mu = PropsSI("V", "P", P, "T", T, fluid)  # dynamic viscosity Pa.s
    nu = mu / rho
    return {"rho": rho, "mu": mu, "nu": nu}

def properties_at_STP(fluid):
    """Return properties near standard conditions (1 atm, 20°C) useful for gases demo."""
    P = 101325.0
    T = 293.15
    return properties_PT(fluid, P, T)
