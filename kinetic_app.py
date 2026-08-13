import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from pic import make_grid, deposit_charge, field_solver, interpolate_field

st.set_page_config(page_title = "Kinetic PIC", layout="wide")

st.title("Kinetic: 1D electrostatic PIC Plasma Simulation")
st.write("A particle-in-cell (PIC) built from scratch ")
st.write("Feel free to adjust parameters in the sidebar (if i get that far) for the simulation")
st.write("More particles obviously gives a more accurate simulation")
st.write("Sadly, youll only be seeing a few plots (they're still pretty cool) instead of a cool 2d/3d real time rendering")

st.write("Watch electrons oscillate at the plasma frequency, or set up two counter steaming electron beams"
         "and watch the two stream instability grow into phase-space vortices")
# side bar time
st.sidebar.header("Simulation parameters")
N = st.sidebar.slider("Particles (N)" , 1000, 200_000, 50_000, step=1000)
Ng = st.sidebar.select_slider("Number of Grid Cells (Ng)", options=[32, 64, 128, 256], value=64)
n_steps = st.sidebar.slider("Number of steps", 100, 1000, 400, step=50)
pert_amplitude = st.sidebar.slider("Perturbation amplitude", 0.001, 0.1, 0.01, step=0.001, format="%.3f")
dt = st.sidebar.slider("Temporal Resolution (dt)", 0.01, 0.10, 0.05, step=0.01)




# Fixed physical constants

L = 2 * np.pi
q_per = -L / N

# derivied quantities
dx, x_grid, k, k_safe = make_grid(L, Ng)
# run the sim
if st.button("run simulation", type="primary"):
    with st.spinner("simulating..."):
        rng = np.random.default_rng(seed=67)
        positions = rng.uniform(0, L, N)
        velocities = rng.normal(0, 0.1, N)

        #seed perturbation
        positions = (positions + pert_amplitude * np.cos(positions)) % L

        #leap frog

        rho0 = deposit_charge(positions, Ng, dx, q_per)
        E0 = field_solver(rho0, k_safe)
        Ep0 = interpolate_field(E0, positions, Ng, dx)
        velocities += 0.5 * Ep0 * dt

        # main PIC loop
        field_energy = np.zeros(n_steps)
        for step in range(n_steps):
            rho = deposit_charge(positions, Ng, dx, q_per)
            E = field_solver(rho0, k_safe)
            Ep = interpolate_field(E, positions, Ng, dx)
            velocities += -Ep * dt
            positions += velocities * dt
            positions = positions % L # wrap case
            field_energy[step] = 0.5 * np.sum(E**2) * dx

    # plot result pls
    t = np.arange(n_steps) * dt
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(t, field_energy)
    ax.set_xlabel("t")
    ax.set_ylabel("field energy")
    ax.set_title("Plasma Oscillation")
    st.pyplot(fig)

    st.success(f"Ran {n_steps} steps with {N} particles")

else:
    st.info("Womp Womp: Adjust parameters or something? idk")

