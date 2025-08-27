# app/viz/plots.py
import numpy as np
import matplotlib.pyplot as plt
from core import pipe_calc

def moody_background(fluid="Fluid", D_vals=None, eps_rel=1e-5):
    """
    Create arrays for a simple moody-like background using Swamee-Jain over a grid.
    Returns Re_grid, f_grid arrays suitable to contour or plot curves.
    (This is a simple quick background for visualization.)
    """
    Re_range = np.logspace(2, 8, 200)
    f_vals = []
    for Re in Re_range:
        f = pipe_calc.friction_factor(Re, eps_rel, 0.1)  # D used only in relative term; placeholder D
        f_vals.append(f)
    return Re_range, np.array(f_vals)

def plot_moody_with_point(Re_point, f_point, title="Moody diagram", show=True):
    Re_range, f_vals = moody_background()
    fig, ax = plt.subplots(figsize=(7,5))
    ax.loglog(Re_range, f_vals, '-', label="approx friction (Swamee-Jain)")
    ax.scatter([Re_point], [f_point], color='red', zorder=10, label=f"Operating point (Re={Re_point:.2e}, f={f_point:.4f})")
    ax.set_xlabel("Reynolds number, Re")
    ax.set_ylabel("Darcy friction factor, f")
    ax.set_title(title)
    ax.grid(which='both', linestyle='--', linewidth=0.5)
    ax.legend()
    if show:
        plt.show()
    return fig
