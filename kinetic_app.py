import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

from sims import run_plasma_oscillation, run_two_stream
from pic import two_stream_growth_rate

st.set_page_config(page_title = "Kinetic PIC", layout="wide")

st.title("Kinetic: 1D electrostatic PIC Plasma Simulation")
st.write("A particle-in-cell (PIC) built from scratch ")
st.write("Feel free to adjust parameters in the sidebar for the simulation")
st.write("More particles obviously gives a more accurate simulation")
st.write("Sadly, youll only be seeing a few plots (they're still pretty cool) instead of a cool 2d/3d real time rendering")

st.write("Watch electrons oscillate at the plasma frequency, or set up two counter streaming electron beams"
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
k = 2 * np.pi / L
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
        ax.semilogy(t, field_energy, label=f"simulated")
        # overlay theoretical grwoth rate for comparison
        gamma = two_stream_growth_rate(k, v0)
        fit_start = n_steps // 10
        fit_end = 3 * (n_steps // 4)
        t_ref = t[fit_start:fit_end]
        log_E_ref = np.log(field_energy[fit_start:fit_end])

        #fit a straight line to log(E) in growth window
        slope, intercept = np.polyfit(t_ref, log_E_ref, deg = 1)
        gamma_measured = slope/2

        W_fit = np.exp(slope * t_ref + intercept)

        if not np.isnan(gamma):
            W_ref = field_energy[fit_start] * np.exp(2 * gamma * (t_ref - t_ref[0]))
            ax.semilogy(t_ref, W_ref, "--", label=f"theory: exp(2 * {gamma:.3f} * t)")

        ax.semilogy(t_ref, W_fit, ":", label=f"Measured from Sim gamma = {gamma_measured:.3f}")

        ax.legend()
        ax.set_ylabel("field energy (log scale)")



    else:
        ax.plot(t, field_energy, label="simulated")

        #measure oscillation frequency from field energy peaks
        # use the prominence function from scipi to ignore noise ripples

        peaks, _ = find_peaks(field_energy, prominence=0.1 * np.max(field_energy))

        if len(peaks) >= 2:
            period_measured = np.mean(np.diff(peaks)) * dt
            freq_measured = 2 * np.pi / period_measured
        else:
            freq_measured = None

        freq_theory = 2.0 # field energy should oscillate at 2 * omega_p which I confirmed in phase 2/3 to be equal to 2.0

        # mark the peaks for easier visuals

        if len(peaks) >= 2:
            ax.plot(t[peaks], field_energy[peaks], "rx", markersize = 8, label="detected peaks")
        ax.set_ylabel("field energy")
        ax.legend()

    ax.set_xlabel("t")
    ax.set_title(mode)
    st.pyplot(fig)
    if mode == "Two Stream Instability":
        st.markdown("""
        **What this shows:** Two counter streaming electron beams at unstable. One small perturbation grows exponentially over time, converting energy from the beams' ordered motion 
        into the electric field.
        - **Simulation output:** (Solid blue line) shows the field energy from the PIC loop on log scale
        - **Theory Prediction:** (dashed): physics (cold plasma dispersion theory) predicts this growth 
        - **Measured from simulation** (dotted) is a straight line fit to the plot derived from the simulated measurements. Its slope/2 (in theory) should give us the real growth rate

        the measurements are also outputted below
        """)
    elif mode == "Plasma Oscillation":
        st.markdown("""
    **What this shows**: Plasma electrons are perturbed slightly from eqiulibrium. Then the system tries to correct itself but because electrons have mass, they overshoot (similar to a mass on a spring).
    They oscillate at the plasma frequency w_p or omega_p (i might have used both in my code).

    It is interesting to note that the field energy is actually twice the plasma frequency because energy ~ E (electric field) squared. Squaring doubles frequency.
    In the normalized units of mine, w_p = 1, so the expected measured frequency is 2. 
    Red Xs mark the peaks.
""")

    # Phase space

    if snapshots is not None:
        fig, axes = plt.subplots(1,4, figsize=(20,5))
        titles = ["initial", "early growth", "late growth", "saturation"]
        for ax, x, v, title in zip(axes, snapshots["x"], snapshots["v"], titles):
            ax.scatter(x,v,s=0.2, alpha = 0.4)
            ax.set_xlabel("x")
            ax.set_ylabel("v")
            ax.set_title(title)
        plt.tight_layout()
        st.pyplot(fig)

    st.success(f"Ran {n_steps} steps with {N} number of particles.")
# measurements
    if mode == "Two Stream Instability": 
        col1, col2, col3 = st.columns(3)
        col1.metric(f"Measured Gamma", f"{gamma_measured:.3f}")
        if not np.isnan(gamma):
            col2.metric("Theory Gamma", f"{gamma:.3f}")
            col3.metric("Error", f"{abs(gamma_measured - gamma) / gamma * 100:.1f}%")
        else:
            col2.metric("Theory Gamma", "stable")
            col3.metric("Error", "—")
    elif mode == "Plasma Oscillation":
        if freq_measured is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("Measured omega", f"{freq_measured:.3f}")
            col2.metric("Theory 2 omega_p", f"{freq_theory:.3f}")
            col3.metric("Error", f"{abs(freq_measured - freq_theory) / freq_theory * 100:.1f}%")
        else:
            st.warning("Not enough oscillation peaks detected, try increasing n_steps or pert_amplitude")



else:
    st.info("Adjust parameters in the sidebar and click **Run simulation**")
