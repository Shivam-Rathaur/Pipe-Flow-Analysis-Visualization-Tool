# app/core/pipe_calc.py
"""
Core pipe-flow calculations:
- Reynolds number
- friction factor (laminar, Swamee-Jain, Colebrook iterative fallback)
- Darcy-Weisbach head loss
- minor losses & pressure drop
All inputs are SI (m, kg, s, Pa).
"""

import math

g = 9.80665  # gravity m/s2

def reynolds_number(rho, V, D, mu=None, nu=None):
    """
    rho: density [kg/m3]
    V: velocity [m/s]
    D: diameter [m]
    mu: dynamic viscosity [Pa.s] (optional)
    nu: kinematic viscosity [m2/s] (optional)
    returns Re
    """
    if nu is None:
        if mu is None:
            raise ValueError("Provide mu or nu")
        nu = mu / rho
    return V * D / nu

def friction_factor_laminar(Re):
    """Laminar friction factor (valid Re < 2300)."""
    return 64.0 / Re

def friction_factor_swamee_jain(Re, eps_rel, D):
    """
    Swamee-Jain explicit approximation for turbulent flow.
    eps_rel: roughness [m]
    D: diameter [m]
    returns f
    """
    # avoid negative or zero
    if Re <= 0:
        raise ValueError("Re must be positive for Swamee-Jain")
    A = eps_rel / D / 3.7
    B = 5.74 / (Re ** 0.9)
    f = 0.25 / (math.log10(A + B) ** 2)
    return f

def friction_factor_colebrook(Re, eps_rel, D, f0=0.02, max_iter=50, tol=1e-6):
    """
    Solve Colebrook-White equation iteratively for turbulent flow:
    1/sqrt(f) = -2 log10(eps/(3.7D) + 2.51/(Re*sqrt(f)))
    Returns f
    """
    if Re <= 0:
        raise ValueError("Re must be positive for Colebrook")
    f = f0
    for i in range(max_iter):
        lhs = 1.0 / math.sqrt(f)
        rhs = -2.0 * math.log10((eps_rel / D) / 3.7 + 2.51 / (Re * math.sqrt(f)))
        residual = lhs - rhs
        # derivative approx for Newton step: df ~ ...
        # Use simple relaxation update:
        f_new = 1.0 / (rhs ** 2)
        if abs(f_new - f) < tol:
            return f_new
        f = 0.5 * (f + f_new)
    return f  # best effort

def friction_factor(Re, eps_rel, D):
    """
    Combined friction factor selection:
    - If laminar (Re < 2300): use laminar formula
    - Else turbulent: first try Swamee-Jain, fallback to Colebrook if invalid
    """
    if Re <= 0:
        raise ValueError("Re must be positive")
    if Re < 2300:
        return friction_factor_laminar(Re)
    # turbulent
    try:
        f_sj = friction_factor_swamee_jain(Re, eps_rel, D)
        if f_sj > 0 and f_sj < 1:
            return f_sj
    except Exception:
        pass
    # fallback
    return friction_factor_colebrook(Re, eps_rel, D)

def velocity_from_flowrate(Q, D):
    """Q [m3/s], D [m] -> average velocity V [m/s]"""
    A = math.pi * (D ** 2) / 4.0
    return Q / A

def head_loss_darcy(f, L, D, V):
    """Darcy-Weisbach head loss h_f (m)"""
    return f * (L / D) * (V ** 2) / (2.0 * g)

def minor_loss_head(K_total, V):
    """Minor losses expressed as head (m). K_total is sum of K coefficients"""
    return K_total * (V ** 2) / (2.0 * g)

def pressure_drop(rho, head_total):
    """Convert head (m) to pressure drop (Pa)"""
    return rho * g * head_total

def analyze_pipe_flow(Q=None, V=None, D=None, L=None, eps_rel=1e-5,
                      rho=None, mu=None, nu=None, K_total=0.0):
    """
    High-level helper:
    Provide Q (m3/s) or V (m/s). D [m], L [m], eps_rel [m], rho [kg/m3], mu [Pa.s] or nu [m2/s].
    Returns dict with Re, f, V, h_f, h_minor, head_total, deltaP.
    """
    if Q is None and V is None:
        raise ValueError("Provide Q or V")
    if V is None:
        V = velocity_from_flowrate(Q, D)
    if rho is None:
        raise ValueError("rho required")
    Re = reynolds_number(rho, V, D, mu=mu, nu=nu)
    f = friction_factor(Re, eps_rel, D)
    h_f = head_loss_darcy(f, L, D, V)
    h_minor = minor_loss_head(K_total, V)
    head_total = h_f + h_minor
    deltaP = pressure_drop(rho, head_total)
    return {
        "Re": Re,
        "f": f,
        "V": V,
        "h_f": h_f,
        "h_minor": h_minor,
        "head_total": head_total,
        "deltaP": deltaP
    }
