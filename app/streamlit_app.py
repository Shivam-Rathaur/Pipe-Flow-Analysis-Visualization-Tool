# app/streamlit_app.py
import streamlit as st
from fluid.fluid_props import properties_PT
from core.pipe_calc import analyze_pipe_flow, velocity_from_flowrate
from viz.plots import plot_moody_with_point
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pipe Flow Tool", layout="wide")
st.title("Pipe Flow Analysis & Visualization Tool")

# sidebar inputs
with st.sidebar:
    fluid = st.selectbox("Fluid", ["Water", "Air", "Nitrogen", "CO2"])
    P = st.number_input("Pressure (Pa)", value=101325.0)
    T = st.number_input("Temperature (K)", value=300.0)
    D = st.number_input("Diameter (m)", value=0.05)
    L = st.number_input("Length (m)", value=10.0)
    eps = st.number_input("Roughness (m)", value=1e-5, format="%.6g")
    mode = st.radio("Input mode", ["Q (m3/s)", "V (m/s)"])
    if mode.startswith("Q"):
        Q = st.number_input("Flow rate Q (m3/s)", value=0.01)
        V = None
    else:
        V = st.number_input("Velocity V (m/s)", value=1.0)
        Q = None
    K = st.number_input("Minor loss coefficient K_total", value=0.0)

# compute props
try:
    props = properties_PT(fluid, P, T)
except Exception as e:
    st.error(f"Fluid property lookup failed: {e}")
    st.stop()

rho = props["rho"]
mu = props["mu"]

if mode.startswith("Q"):
    res = analyze_pipe_flow(Q=Q, D=D, L=L, eps_rel=eps, rho=rho, mu=mu, K_total=K)
else:
    res = analyze_pipe_flow(V=V, D=D, L=L, eps_rel=eps, rho=rho, mu=mu, K_total=K)

st.subheader("Results")
st.write({
    "Fluid": fluid,
    "Re": res["Re"],
    "f": res["f"],
    "V (m/s)": res["V"],
    "Head (m)": res["head_total"],
    "Pressure drop (Pa)": res["deltaP"]
})

# Moody plot
fig = plot_moody_with_point(res["Re"], res["f"], title=f"Moody diagram — {fluid}", show=False)
st.pyplot(fig)
