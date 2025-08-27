# app/cli.py
"""
Simple CLI to compute pipe flow using CoolProp for fluid props.
Example:
  python app/cli.py --fluid Water --mode Q --Q 0.01 --D 0.05 --L 10 --eps 1e-5 --T 300 --P 101325
"""
import argparse
from fluid.fluid_props import properties_PT
from core.pipe_calc import analyze_pipe_flow

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fluid", type=str, default="Water")
    p.add_argument("--mode", choices=["Q","V"], default="Q", help="Q: flowrate m3/s, V: velocity m/s")
    p.add_argument("--Q", type=float, help="Volumetric flow rate m3/s")
    p.add_argument("--V", type=float, help="Velocity m/s")
    p.add_argument("--D", type=float, required=True, help="Diameter [m]")
    p.add_argument("--L", type=float, required=True, help="Length [m]")
    p.add_argument("--eps", type=float, default=1e-5, help="Absolute roughness [m]")
    p.add_argument("--T", type=float, default=300.0, help="Temperature [K]")
    p.add_argument("--P", type=float, default=101325.0, help="Pressure [Pa]")
    p.add_argument("--K", type=float, default=0.0, help="Total minor loss coefficient")
    args = p.parse_args()

    # get fluid props
    props = properties_PT(args.fluid, args.P, args.T)
    rho = props["rho"]
    mu = props["mu"]
    # compute from Q or V
    if args.mode == "Q":
        if args.Q is None:
            p.error("--Q required for mode Q")
        res = analyze_pipe_flow(Q=args.Q, D=args.D, L=args.L, eps_rel=args.eps, rho=rho, mu=mu, K_total=args.K)
    else:
        if args.V is None:
            p.error("--V required for mode V")
        res = analyze_pipe_flow(V=args.V, D=args.D, L=args.L, eps_rel=args.eps, rho=rho, mu=mu, K_total=args.K)

    # print
    print(f"Fluid: {args.fluid}, P={args.P} Pa, T={args.T} K")
    print(f"Re: {res['Re']:.3e}")
    print(f"Friction factor f: {res['f']:.6f}")
    print(f"Velocity V: {res['V']:.4f} m/s")
    print(f"Head loss (major): {res['h_f']:.6f} m")
    print(f"Head loss (minor): {res['h_minor']:.6f} m")
    print(f"Total head: {res['head_total']:.6f} m")
    print(f"Pressure drop: {res['deltaP']:.2f} Pa")

if __name__ == "__main__":
    main()
