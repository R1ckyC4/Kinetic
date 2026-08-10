import numpy as np
import matplotlib.pyplot as plt
print("starting...")





# parameters
N = 10 ** 7 # number of macro parts
Ng = 256 # num of grid cells

L = 2 * np.pi

dt = 0.05

n_steps = 500

# Grid
dx = L / Ng # grid spacing

x_grid = np.arange(Ng) * dx

# inital conds
rng = np.random.default_rng(seed=67)
positions = rng.uniform(0,L,N)
velocities = rng.normal(0,0.1,N)

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
positions_pert = (positions + pert_amplitude * np.cos(positions)) % L
rho_p = deposit_charge(positions_pert)
E_p = field_solver(rho_p)

fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(x_grid,rho_p)
axes[0].set_ylabel("rho")

axes[0].set_title("Density after Perturbation")
axes[1].plot(x_grid, E_p)
axes[1].set_xlabel('x')
axes[1].set_title('Electric field')
plt.tight_layout()
plt.show()