# Pipe Flow Analysis & Visualization Tool

## 📌 Project Overview
This project is a **Python-based engineering tool** for analyzing and visualizing fluid flow in pipes.
It applies core principles of **thermodynamics and fluid dynamics** to calculate Reynolds number, friction factor, pressure drop, and head losses using the **Darcy–Weisbach equation**.

The tool was built with industrial R&D applications in mind, aligning with **product development and simulation practices** in plant engineering, combustion systems, and process machinery.

---

## ⚙️ Features
- **Core Calculations**
  - Reynolds number
  - Friction factor (Laminar, Swamee–Jain, Colebrook iterative solver)
  - Darcy–Weisbach head loss
  - Minor losses via K-values
  - Pressure drop conversion

- **Fluid Properties (via CoolProp)**
  - Density, dynamic viscosity, kinematic viscosity from P–T inputs
  - Pre-configured fluids: Water, Air, Nitrogen, CO₂

- **Visualization**
  - Moody diagram with system operating point
  - Flow regime identification (laminar, transition, turbulent)

- **Interfaces**
  - **Command-Line Interface (CLI):** quick engineering calculations
  - **Streamlit Web App:** interactive interface with real-time plots

---

## 🛠️ Tech Stack
- Python
- CoolProp – fluid thermophysical properties
- NumPy & Matplotlib – numerical handling and visualization
- Streamlit – interactive web app

---

## 📂 Project Structure
```

pipe\_flow\_tool/
├─ requirements.txt
├─ README.md
├─ app/
│  ├─ init.py
│  ├─ streamlit\_app.py       \# Web UI
│  ├─ cli.py                 \# Command-line interface
│  ├─ core/
│  │  └─ pipe\_calc.py        \# Core fluid mechanics equations
│  ├─ fluid/
│  │  └─ fluid\_props.py      \# CoolProp wrapper
│  ├─ viz/
│  │  └─ plots.py            \# Moody plot & visualization

````
---

## 🚀 Usage

### 1. Command Line
```bash
# Example: water flow in 5 cm dia pipe, 10 m length, flowrate 0.01 m³/s
python app/cli.py --fluid Water --mode Q --Q 0.01 --D 0.05 --L 10 --T 300 --P 101325
````

### 2\. Streamlit Web App

```bash
streamlit run app/streamlit_app.py
```

-----

## 🎯 Relevance to Product Development

This project demonstrates skills aligned with industrial product R\&D:

  - **Thermodynamics & Fluid Dynamics** – implemented fundamental flow models
  - **Simulation & Numerical Analysis** – iterative solvers and CFD-inspired calculations
  - **Engineering Design Insight** – adaptable to combustion, piping, and plant design
  - **Visualization & Validation** – Moody diagram and flow regime interpretation

-----

## 📖 Learning Outcomes

  - Application of classroom knowledge to real-world engineering design
  - Deeper understanding of structural, thermal, and fluid analysis
  - Experience in building simulation-oriented tools for product development

-----

## 💡 Future Extensions

  - Integration with CFD solvers (e.g., STAR-CCM+, ANSYS Fluent)
  - Database of standard roughness values & K-factors for fittings and valves
  - Extended visualization: velocity profiles, energy grade lines, 3D flow fields

-----

👨‍💻 Author
Shivam Rathaur

B.Tech (3rd Year), Materials Science & Metallurgical Engineering, IIT Hyderabad
(Second Major: Mechanical Engineering)