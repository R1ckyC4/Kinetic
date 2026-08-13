# simulation drivers for the plasma physics aspect of kinetic. UI will call these
# sims.py will call from pic.py


import numpy as np
from pic import make_grid, deposit_charge, field_solver, interpolate_field 

def run_plasma_oscillation(N, Ng, dt, n_steps, pert_amplitude, L= 2 * np.pi, seed = 67):
    """Run the plasma oscillation test. Return (t, field_energy)"""
    q_per = -L / N
    dx, x_grid, k , k_safe = make_grid(L, Ng)

    rng = np.random.default_rng(seed=seed)
    positions = rng.uniform(0, L, N)
    velocities = rng.normal(0 ,0.1, N)

    # Seed perturbation
    positions = (positions + pert_amplitude * np.cos(positions)) % L

    #leap frong

    rho0 = deposit_charge(positions, Ng, dx, q_per)
    E0 = field_solver(rho0, k_safe)
    Ep0 = interpolate_field (E0, positions, Ng, dx)
    velocities += 0.5 * -Ep0 * dt 

    # Main loop
    field_energy = np.zeros(n_steps)
    for step in range(n_steps):
        rho = deposit_charge(positions, Ng, dx, q_per)
        E = field_solver(rho, k_safe)
        Ep = interpolate_field(E, positions, Ng, dx)
        velocities = -Ep * dt
        positions += velocities * dt
        positions = positions % L # wrap around 

        field_energy[step] = 0.5 * np.sum(E**2) * dx

    t = np.arange(n_steps) * dt
    return t, field_energy

def run_two_stream(N, Ng, dt, n_steps, pert_amplitude, v0, L = 2* np.pi, seed = 67):
    """Run the two stream instability simulation. Return t, field energy, snapshots"""
    q_per = -L / N
    dx, x_grid, k, k_safe = make_grid(L, Ng)

    rng = np.random.default_rng(seed=seed)
    positions = rng.uniform(0,L,N)
    velocities = np.where(np.arange(N) < N // 2, v0, -v0)
    velocites += rng.normal(0, 0.01, N) # small thermal spread

    positions = (positions + pert_amplitude * np.cos(positions)) % L
    rho0 = deposit_charge(positions, Ng, dx, q_per)
    E0 = field_solver(rho0, k_safe)
    Ep0 = interpolate_field(E0, positions, Ng, dx)
    velocities += 0.5 * Ep0 * dt

    field_energy = np.zeros(n_steps)
    snapshot_steps = [0, n_steps // 3, 2 * n_steps // 3, n_steps - 1]
    snapshots = {"x": [], "v": []}
    
    for step in range(n_steps):
        rho = deposit_charge(positions, Ng, dx, q_per)
        E = field_solver(rho, k_safe)
        Ep = interpolate_field(E, positions, Ng, dx)
        velocities += -Ep * dt
        positions += velocities * dt
        positions = positions % L
        field_energy[step] = 0.5 * np.sum(E**2) * dx
        
        if step in snapshot_steps:
            snapshots["x"].append(positions.copy())
            snapshots["v"].append(velocities.copy())
    
    t = np.arange(n_steps) * dt
    return t, field_energy, snapshots
