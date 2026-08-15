import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from sims import run_plasma_oscillation, run_two_stream

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
mode = st.sidebar.selectbox("Simulation mode", ["Plasma Oscillation", "Two Stream Instability"])

N = st.sidebar.slider("Particles (N)" , 1000, 200_000, 50_000, step=1000)
Ng = st.sidebar.select_slider("Number of Grid Cells (Ng)", options=[32, 64, 128, 256], value=64)
n_steps = st.sidebar.slider("Number of steps", 100, 1000, 400, step=50)
dt = st.sidebar.slider("Time step (dt)", 0.01, 0.10, 0.05, step=0.01)
pert_amplitude = st.sidebar.slider("Perturbation amplitude", 0.001, 0.1, 0.01, 
                                    step=0.001, format="%.3f")

if mode == "Two Stream Instability":
    v0 = st.sidebar.slider("Beam velocity (v0)", 0.1, 1.5, 1.0/np.sqrt(2), step=0.05)




# Fixed physical constants

L = 2 * np.pi
q_per = -L / N

# run the sim
if st.button("run simulation", type="primary"):
    with st.spinner("simulating..."):
        if mode == "Plasma Oscillation":
            t, field_energy = run_plasma_oscillation(N, Ng, dt, n_steps, pert_amplitude)
            snapshots = None
        else: t , field_energy, snapshots = run_two_stream(N, Ng, dt, n_steps, pert_amplitude, v0)

    # Field energy plot
    fig, ax = plt.subplots(figsize=(10,5))
    if mode == "Two Stream Instability":
        ax.semilogy(t, field_energy)
        ax.set_ylabel("field energy (log scale)")


    else:
        ax.plot(t, field_energy)
        ax.set_ylabel("field_energy")
    ax.set_xlabel("t")
    ax.set_title(mode)
    st.pyplot(fig)

    # Phase space

    if snapshots is not None:
        fig, axes = plt.subplots(1,4, figsize=(20,5))
        titles = ["inital", "early growth", "late growth", "saturation"]
        for ax, x, v, title in zip(axes, snapshots["x"], snapshots["v"], titles):
            ax.scatter(x,v,s=0.2, alpha = 0.4)
            ax.set_xlabel("x")
            ax.set_ylabel("v")
            ax.set_title(title)
        plt.tight_layout()
        st.pyplot(fig)

    st.success(f"Ran {n_steps} steps with {N} number of particles.")

else:
    st.info("Adjust parameters in the sidebar and click **Run simulation**")
