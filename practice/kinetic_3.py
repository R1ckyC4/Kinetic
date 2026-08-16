import numpy as np
import matplotlib.pyplot as plt
print("starting...")

from scipy.signal import find_peaks



# parameters
N = 10 ** 6 # number of macro parts
Ng = 64 # num of grid cells

L = 2 * np.pi

dt = 0.05

n_steps = 1000

v0 = 1.0 / np.sqrt(2) # inital beam speed


# Grid
dx = L / Ng # grid spacing

x_grid = np.arange(Ng) * dx

# inital conds
rng = np.random.default_rng(seed=67)
positions = rng.uniform(0,L,N)
# two counter streaming beams / where half of them is v0 and the other half is -v0
velocities = np.where(np.arange(N) < N // 2, v0, -v0)

# notes
# I gave the particles their vels based on a gaussian distribution, like the maxwell boltzmaan dist
#rho is charge density

q_per = -L / N # charge per macro particle

#fourier stuff for poisson solve (refer to notes.md on 8/10)
# wavenums for each Fourier mode
#np.fft.fftfreq returns cycles/unit so multiply by 2pi rads

k = 2 * np.pi * np.fft.fftfreq(Ng, d=dx)
k_safe = np.where( k == 0, 1.0, k) # prevent divide by zero





def deposit_charge(positions):
    """
    Spread each particle's charge onto the two nearest grid points using cluod in cell weighting. Returns charge density rho
    """
    rho = np.zeros(Ng)
    # for each parti, find which grid cell its in and where within that cell

    j_float = positions/dx # position in grid units
    j = np.floor(j_float).astype(int) % Ng 
    f = j_float - np.floor(j_float) # fractional distance to the right 
    jp1 = (j+1) % Ng

    #scatter charge to left and right grid points
    np.add.at(rho, j, q_per * (1-f))
    np.add.at(rho, jp1, q_per * (f))

    # convert to charge density (charge per unit length)
    rho /= dx

    rho += 1.0
    # going to treat the protons as a background, just like that one guy with the plum pudding model
    #text book says this is the frozen ion approx or jellium

    return rho

def field_solver(rho):
    """
    Solve poisson's equation for the E field by FFT
    Using the rho as a function of position, return E(x)
    """
    rho_hat = np.fft.fft(rho)
    E_hat = -1j * rho_hat/k_safe #here is where to worry about division by zero
    E_hat[0] = 0.0 # guage choice (idk what this means tbh)
    E = np.real(np.fft.ifft(E_hat))
    return E


def interpolate_field(E, positions):
    """
    Sample the grid E field at each particles postition using CIC. Testing out symmetric weights to prevent self force and preserve momentum
    """
    j_float = positions / dx 
    j = np.floor(j_float).astype(int) % Ng
    f = j_float - np.floor(j_float)
    jp1 = (j + 1) % Ng
    return (1 - f) * E[j] + f * E[jp1]




# Testing
print(f"total particles = {N}")


# Test 1


rho = deposit_charge(positions)
E = field_solver(rho)
print(f"uniform: max rho = {np.abs(rho).max()}")

print(f"uniform: max E = {np.abs(E).max()}")

# make a sinusoidal pertubation and check if E is right
# disturb each particle by a small cos pertubation
pert_amplitude = 0.01
positions = (positions + pert_amplitude * np.cos(positions)) % L


#positions_pert = (positions + pert_amplitude * np.cos(positions)) % L
#rho_p = deposit_charge(positions_pert)
#E_p = field_solver(rho_p)

# testing out leapfrog method for simulation
# push velocites backwards by half a step

rho0 = deposit_charge(positions)
E0 = field_solver(rho0)
Ep0 = interpolate_field(E0, positions)
velocities += 0.5 * Ep0 * dt # v(dt/2) = v(0) + d * dt/2 (a ~ -E)
# report back pls
field_energy = np.zeros(n_steps)

# save phase space snapshots at intermediate times between start and end

snapshot_steps = [0, n_steps // 3, 2 * n_steps // 3, n_steps - 1]
snapshot_x = []
snapshot_v = []



# main PIC loop

for step in range(n_steps):
    rho = deposit_charge(positions) # 1. deposit
    E = field_solver(rho) # 2. solve
    Ep = interpolate_field(E,positions) # interpolate
    velocities += - Ep * dt # 4. kick
    positions += velocities * dt # 5. drift
    positions = positions % L # 6. wrap
    field_energy[step] = 0.5 * np.sum(E**2) * dx
    if step in snapshot_steps:
        snapshot_x.append(positions.copy())
        snapshot_v.append(velocities.copy())

# plot 1 field energy log scale
gamma = 0.35

t = np.arange(n_steps) * dt
plt.figure(figsize=(10,5))
plt.semilogy(t,field_energy)
plt.xlabel("t")
plt.ylabel("field energy (log scale)")    
plt.title("2 stream instability: energy growth")

# overlay the predicted growth rate we got from our very rigorous math
t_ref = t[50:400]
W_ref = field_energy[50] * np.exp(2 * gamma * (t_ref - t_ref[0]))
plt.semilogy(t_ref, W_ref, "--", label=f"theory = exp(2*{gamma}*t)")
plt.legend()
plt.show()

# plot 2 - phase space
fig , axes = plt.subplots(1,4, figsize=(20,5))
titles = ["inital", "early growth", "late growth", "saturation"]
for ax , x, v , titles in zip(axes, snapshot_x, snapshot_v, titles):
    ax.scatter(x , v , s=0.2, alpha = 0.4)
    ax.set_xlabel('x')
    ax.set_ylabel('v')
    ax.set_title(titles)
plt.tight_layout()

plt.show()    